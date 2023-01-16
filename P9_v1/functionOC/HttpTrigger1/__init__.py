import logging
import azure.functions as func

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
import scipy
import pickle

from surprise import Reader, Dataset,SVDpp
from io import BytesIO

class ContentBasedRecommender:
    '''le fit calcule les users profiles'''
    
    MODEL_NAME = 'Content-Based'
    

    def __init__(self,data_map,i2vec,dic_ri,dic_ir,profils):
        '''constructeur'''
        #dico inner raw iid
        self.dic_ir = dic_ir
        #dico raw inner iid
        self.dic_ri = dic_ri
        self.items_embedding = i2vec
        #les train interactions servent à:
            #calculer les profils
            #ignorer les interactions dans la reco
        self.train_user_interact = data_map
        self.user_profiles = profils
    
    
    def get_model_name(self):
        '''renvoie le nom du modèle'''
        return self.MODEL_NAME
    

    def _get_similar_items_to_user_profile(self, uid):#, topn=100000):
        '''renvoie une liste d items similaires au profil de l'uid
            liste de couples (raw iid, cosine) triés par cosine decroissant'''
        #on calcul distances profil uid vs articles : sous forme 2D 1 ligne / nombre iid colonnes dans l'ordre inner du wemb
        cosine_similarities = cosine_similarity(self.user_profiles[uid], self.items_embedding)
        #on tri par distance: argsort donne les indices par scores croissants /flatten pour passer en 1D
        #on recupère un array des inner_iid de taille topn : les plus proches du profil sont à droite
        similar_indices = cosine_similarities.argsort().flatten()#[-topn:]
                                                        ################################################################################
        #on tri : sorted(iterable, key=None, reverse=False)
        # l'iterable est une liste de couples (raw_iid, cosine similarites)
        #on tri par similarité décroissante
        similar_items = [(self.dic_ir[i], cosine_similarities[0,i]) for i in similar_indices[::-1]]
        return similar_items
    
    #methode qui recommande en ignorant les articles deja vus
    def recommend_items(self, uid, topn=5):
        '''renvoie une liste de reco similaires au profil de l uid
            triés par cosine decroissant
             sans les interactions du train
                sous forme de dataframe'''
        #on recupere la liste brute de 1200 reco classés par cosine decroissant
        similar_items = self._get_similar_items_to_user_profile(uid)
        #on recupere la liste des iid a ignorer car deja vus
        #items_to_ignore = self.train_user_interact.loc[self.train_user_interact.user_id==uid,"article_id"].tolist()
        items_to_ignore = set(self.train_user_interact.loc[self.train_user_interact.user_id==uid].article_id)
        #on enleve les deja vus
        #similar_items_filtered = list(filter(lambda x: x[0] not in items_to_ignore, similar_items))
        recommendations_df = pd.DataFrame(similar_items, columns=['article_id', 'cb_cosine_with_profile'])
        reco = recommendations_df.loc[recommendations_df.article_id.isin(items_to_ignore)==False].copy()
        if topn>0:
            reco=reco.head(topn)
        return reco


class CollabFiltRecommender:
    
    MODEL_NAME = 'Collaborative-Filtering-SVDpp'
    
    #constructeur
    def __init__(self,algo,data_map):
        '''constructeur'''
        #les train interactions servent à:
            #calculer les profils
            #ignorer les interactions dans la reco
        #self.train_user_interact = data_map
        self.algo=algo
        self.train_user_interact = data_map
        
    #methode qui renvoie le nom du modele    
    def get_model_name(self):
        return self.MODEL_NAME
        
    def recommend_items(self,uid,topn=5):
        '''renvoie une liste de prediction pour un uid
            le SVD ne peut sortir des prédictions que pour les uid et iid dispo dans le train'''
        #prediction fonctionne avec les raws id
        #https://towardsdatascience.com/difference-between-apply-and-transform-in-pandas-242e5cf32705
        iid_to_ignore=set(self.train_user_interact.loc[self.train_user_interact.user_id==uid].article_id)
        items2pred=pd.DataFrame(set(self.train_user_interact.article_id)-iid_to_ignore,columns=['article_id'])
        items2pred['pred']=items2pred['article_id'].apply(lambda x:self.algo.predict(uid=uid, iid=x)[3])
        #pred['detail']=pred['article_id'].apply(lambda x:cf.predict(uid=uid, iid=x)[4])
        if topn==0:
            recommendations_df=items2pred.loc[:,['article_id','pred']].sort_values(by='pred', ascending=False)
        else:
            recommendations_df=items2pred.loc[:,['article_id','pred']].sort_values(by='pred', ascending=False).head(topn)

        return recommendations_df

class PopularityFiltRecommender:
    
    MODEL_NAME = 'Popularity-Filtering'
    
    #constructeur
    def __init__(self,data_map):
        '''constructeur'''
        self.train_user_interact = data_map
        
    #methode qui renvoie le nom du modele    
    def get_model_name(self):
        return self.MODEL_NAME
    
    #fit du modèle
    def fit(self):
        self.raw_reco=self.train_user_interact[['nb','article_id']].groupby(['article_id']).sum().sort_values(by=['nb'],ascending=False).reset_index()

    def recommend_items(self,uid,topn=5):
        '''renvoie une liste de prediction pour un uid'''
        if topn==0:
            recommendations_df=self.raw_reco
        else:
            recommendations_df=self.raw_reco.head(topn)
        return recommendations_df

class HybridRecommender:
    
    MODEL_NAME = 'Hybrid-Filtering'
    
    #constructeur
    def __init__(self,data_map,i2vec,dic_ri,dic_ir, profils, algo):
        '''constructeur'''
        self.train_user_interact = data_map
        self.dic_ir = dic_ir
        self.dic_ri = dic_ri
        self.items_embedding = i2vec
        self.user_profiles = profils
        self.algo=algo
    
    def get_model_name(self):
        return self.MODEL_NAME
    
    #fit du modèle
    def fit(self):
        '''le fit consiste a fitter les sous modèles'''
        self.cf_model = CollabFiltRecommender(self.algo,self.train_user_interact)
        self.cb_model = ContentBasedRecommender(self.train_user_interact,self.items_embedding,self.dic_ri,self.dic_ir,self.user_profiles)
        self.pf_model = PopularityFiltRecommender(self.train_user_interact)
        self.pf_model.fit()
        
    def recommend_items(self,uid,topn=5):
        '''renvoie une liste de prediction pour un uid'''
        #si uid pas connu du train: seul le popularity recommander fonctionne dans notre cas
        #on pourrait également concevoir un social reco basé sur un social profil, encore faudrait il avoir assez d 'infos'
        if uid not in set(self.train_user_interact.user_id):
            #parfait quand l'uid n'est pas connu du train, n a pas  d'interactions
            reco=self.pf_model.recommend_items(uid,0)
        else:
                # content based : permet de donner des iid qui n'ont pas d'interactions mais qui étaient disponibles
            reco_cb=self.cb_model.recommend_items(uid,0)
                # pour la normalisation, le but est de garder les meilleurs, donc les outliers positifs
                #il vaut mieux dans ce cas diviser par le max que par une standard deviation 
                #qui ne rendra pas forcement les outliers similaires entre facteurs pour une pondéaration
            #reco_cb['norm_cb']=(reco_cb.cb_cosine_with_profile-reco_cb.cb_cosine_with_profile.median())/(reco_cb.cb_cosine_with_profile.max()-reco_cb.cb_cosine_with_profile.median())
            reco_cb['rank_cb']=reco_cb.cb_cosine_with_profile.rank(ascending=False)
                # donne de bons resultats mais necessite des uid et des iid qui ont des interactions dans le train
            reco_cf=self.cf_model.recommend_items(uid,0)
            #reco_cf['norm_cf']=(reco_cf.pred-reco_cf.pred.median())/(reco_cf.pred.max()-reco_cf.pred.median())
            reco_cf['rank_cf']=reco_cf.pred.rank(ascending=False)
                #comment les pondérer? 80/20 normalisé par exemple?
                #en gros la pondération est anecdotique: on privilegie CF et quand on a pas de CF, on met la note de CB
            reco = reco_cb.merge(reco_cf,how='outer', on='article_id')
                #on fill les norm_cf vides (iid inconnu du train) par norm_cv avant pondération
                #on pourait également filler les iid peu interagis afin de favoriser le content dans ce cas la
            reco.loc[reco['rank_cf'].isnull(),'rank_cf'] = reco['rank_cb']
            reco['rank']=0.99999*reco['rank_cf']+0.00001*reco['rank_cb']
            
            reco=reco.sort_values(by='rank', ascending=True)


        if topn==0:
            recommendations_df=reco
        else:
            recommendations_df=reco.head(topn)
            
        return recommendations_df.reset_index(drop=True)
        #return recommendations_df

def main(
    req: func.HttpRequest,
    all: func.InputStream) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not req:
            logging.info('req pas ok')
    if not all:
            logging.info('all pas ok')
    #load data
    name = req.params.get('name')
    blob_to_read = BytesIO(all.read())

    with blob_to_read as file:
        algo_ = pickle.load(file)
        data_map_ = pickle.load(file)
        items_df_ = pickle.load(file)
        i2vec_ = pickle.load(file)
        dic_ir_= pickle.load(file)
        dic_ri_ = pickle.load(file)
        profils_= pickle.load(file)
    
    #le mieux est de post {'userId', 'valeur'}
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            #name = req_body.get('name')
            name = req_body.get('userId')

    if name:
        hr_model = HybridRecommender(data_map_,i2vec_,dic_ri_,dic_ir_,profils_,algo_)
        hr_model.fit()
        top5=hr_model.recommend_items(int(name)).article_id.to_list()
        #top5=[dic_ri_[7]]
        #print(top5)
        return func.HttpResponse(f"{top5}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
