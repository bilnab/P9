import logging
import azure.functions as func
#import scipy
import pickle
#import pandas as pd
#import numpy as np
#
#from sklearn.metrics.pairwise import cosine_similarity
#from sklearn import preprocessing
from surprise import Reader, Dataset
from surprise import SVDpp
from io import BytesIO

def main(req: func.HttpRequest,
    all: func.InputStream
    ) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    blob_to_read = BytesIO(all.read())

    with blob_to_read as file:
        algo_ = pickle.load(file)
        data_map_ = pickle.load(file)
        items_df_ = pickle.load(file)
        i2vec_ = pickle.load(file)
        dic_ir_= pickle.load(file)
        dic_ri_ = pickle.load(file)
        profils_= pickle.load(file)

    #reader = Reader(rating_scale=(0,5))
    ###lecture du train par surprise
    #
    #data = Dataset.load_from_df(data_map_[['user_id','article_id','nb']], reader)
    ###construction du trainset surprise 
    #trainset = data.build_full_trainset()
    #algo2 = SVDpp(n_epochs=20, lr_all=0.007, reg_all=0.1)
    #algo2.fit(trainset)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        #return func.HttpResponse(f"datamap est readable: {[len(pickle.loads(datamap.read()).index),pickle.loads(i2vec.read()).shape,len(pickle.loads(dicri.read())),len(pickle.loads(dicir.read())),len(pickle.loads(profils.read())),(pickle.loads(algo.read()).predict(uid=7, iid=30970)[3])]}.")
        return func.HttpResponse(f"datamap est readable: {[(algo_.predict(uid=7, iid=30970)[3])]}.")
        #return func.HttpResponse(f"datamap est readable")
        #{pickle.format_version}")
        #: {[(algo2.predict(uid=7, iid=30970)[3])]}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
