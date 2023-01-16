import logging

import azure.functions as func


def main(req: func.HttpRequest, recocosmo: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #le passage de parametre du httptrigger au input cosmodb binding se fait dans functions.json
    try:
        #si l'hybride existe
        top5=recocosmo[1]['reco']
        logging.info(recocosmo[1]['reco'])
        pass
    except IndexError:
        #sinon on recupere le popularity
        #dans la requete sql du binding: on prend 2 items en fontion du userid
        #le 0 en chiffre qui stocke par construction le popularity
        #le userid requesté
        top5=recocosmo[0]['reco']
        
    return func.HttpResponse(f"{top5}")
 