# P9  
<img src="/img/azure.png" width="150"> <img src="/img/azf.png" width="150"> <img src="/img/vsc.png" width="150">     
 
**Projet d'application de recommandation de contenu**  
  
L'enjeu consiste à concevoir des scripts permettant de recommander du contenu à ses utilisateurs:  
* Executer une chaine de traitements IA bout en bout
	* conception d'un **MVP** sous forme d'uen application mobile de recommandation de contenu  
	* utiliser une architecture **SERVERLESS** avec des **azure functions** pour faire le lien entre système de recommandation et application  

<img src="/img/reco.png" width="800">

## Ressources:  
[Données utilisateur (interactions, informations sur les articles, sur les sessions utilisateurs) ](https://s3-eu-west-1.amazonaws.com/static.oc-static.com/prod/courses/files/AI+Engineer/Project+9+-+R%C3%A9alisez+une+application+mobile+de+recommandation+de+contenu/news-portal-user-interactions-by-globocom.zip)  
[github de l'application web à utiliser](https://github.com/OpenClassrooms-Student-Center/bookshelf)     
[mode opératoire de l'application web](https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/Ing%C3%A9nieur_IA_P9/Mode+ope%CC%81ratoire+test+Azure+function_V1.1.docx.pdf)           
  
Autres ressources utiles:  
Principe d'un système de recommandation:  
[cours video: Content based Recommender Systems](https://www.youtube.com/watch?v=YMZmLx-AUvY)  
[content based filtering](https://heartbeat.fritz.ai/recommender-systems-with-python-part-i-content-based-filtering-5df4940bd831)  
[collaborative filtering](https://realpython.com/build-recommendation-engine-collaborative-filtering/)  
Azure functions:  
[lien 1](https://www.youtube.com/watch?v=coT4IlGQLCw&list=PLbl2SbVIi-Wo2W81Jyqlv5B375W_EcUsj)  
[lien 2](https://www.youtube.com/watch?v=9RLbuEnW-6g&list=PLbl2SbVIi-Wo2W81Jyqlv5B375W_EcUsj&index=13)  
Web recommandations:  
[Librairie surprise:](https://surprise.readthedocs.io/)  
[Exemple de systeme de reco avec surprise:](https://medium.com/hacktive-devs/recommender-system-made-easy-with-scikit-surprise-569cbb689824)  
[Exemple de reco sur Kaggle:](https://www.kaggle.com/gspmoreira/recommender-systems-in-python-101)  
[Libraire implicit :](https://github.com/benfred/implicit)  
[Liste de modèle de collaborative filtering:](https://github.com/microsoft/recommenders)  
Azure:  
[Bonnes pratiques:](https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/Ing%C3%A9nieur_IA_P1/Bonnes_pratiques_consmmation_Azure.pdf)  
[Azure functions et vscode:]( https://docs.microsoft.com/fr-fr/azure/azure-functions/create-first-function-vs-code-python)  
[Creation azure functions sur azure:]( https://docs.microsoft.com/fr-fr/learn/modules/create-serverless-logic-with-azure-functions/)  
[Liaison d’entrée de blobs dans azure function:]( https://docs.microsoft.com/fr-fr/azure/azure-functions/functions-bindings-storage-blob-input?tabs=python)  
[Liaison d’entrée de cosmo db dans azure function:]( https://docs.microsoft.com/fr-fr/azure/azure-functions/functions-bindings-cosmosdb-v2-input?tabs=python)  
 

## Script
3 notebooks commentés:     
[lien1](/P9_v0.2.ipynb)  
[lien2](/P9_v0.3_wblob.ipynb)  
[lien3](/P9_v0.4_wcosmodb.ipynb)  
et l'appli:
[le rep](/P9_v1)  
  
## Présentation PDF:  
[pdf complet](/P9.pdf)  
<img src="/img/P9%20pres.png" height="300">  

 

