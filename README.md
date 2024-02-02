# Les attaques de requin dans le monde depuis 1800

## Introduction

Dans le jeu de données que nous allons analyser, les informations fournies concernent les attaques de requins répertoriées dans le monde. Nous avons décidé de ne considérer que les données à partir de l'année 1800 en raison du nombre limité d'attaques antérieure à cette date et de la mauvaise qualité de leur enregistrement. Les données sont, selon toute vraisemblance, rentrées manuellement dans le jeu de données, un nettoyage approfondi est donc nécessaire pour plusieurs catégories. Les données disponible pour chaque observation sont:

| Donnée | Description |
| ------ | ------ |
| Date | La date de l'incident |
| Year | L'année de l'incident |
| Type | L'origine de l'incident (provoqué ou non provoqué) |
| Country | Pays |
| Area | État ou département |
| Location | Lieu précis (ville, plage, ...) |
| Activity | Activité faite par la victime lors de l'attaque (plongée, peche, ...) |
| Name | Nom de la victime |
| Sex | Sexe de la victime |
| Age | Age de la victime |
| Injury | Blessure précise de la victime |
| Fatal (Y/N) | Si l'incident a été fatal ou non |
| Time | Heure de l'incident |
| Species | Espèce du requin |

D'autres données sont disponibles comme l'id de l'incident ou la source du rapport, mais nous ne les utiliserons pas ici. Les données proviennent de [kaggle ](https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset).

## User Guide

Pour utiliser ce dashboard, il vous faudra tout d'abord cloner le dépôt Git sur sa machine. Pour cela, vous pouvez vous placer dans le dossier souhaité à l'aide de la commande :
```sh
$ cd /chemin/vers/votre/répertoire/de/projets
```
Puis cloner le dépôt Git avec la commande : 
```sh
$ git clone https://github.com/brieuc060303/Python
```
En cas de problème, vérifiez que vous êtes bien connecté avec vos identifiants Git.
A présent, si vous regardez votre dossier, vous devriez y trouver une copie complète du dépôt Git.
Vous devez alors lancer le fichier requirements.txt qui contient la liste des packages additionnels requis avec la commande :
```sh
$ python -m pip install -r requirements.txt
```
qui installera l’ensemble des dépendances nécessaires.
Vous devrez ensuite télécharger le jeu de donnée avec 
```sh
$ python get_data.py
```
Notez que si vous avez déjà téléchargé le dataset et/ou installé les packages additionnels, vous n'avez pas besoin d'effectuer ces étapes à nouveau. De plus, les données et packages ne seront pas téléchargés plusieurs fois si vous relancez le fichier `get_data.py` ou `requirements.txt`.
Enfin, il vous suffit de lancer le dashboard avec la commande :
```sh
$ python main.py
```
Et vous pourrez y accéder à l'adresse suivante : 
```sh
http://127.0.0.1:8050/
```
Pour stopper le dashboard, vous pouvez utiliser le raccourci `Ctrl + C` dans le terminal où vous l'avez lancé.

##  Rapport d’analyse

#### "Years"
Dans l'onglet "Years", on peut observer l'évolution du nombre d'attaques de requins par année, et l'on remarque que ce nombre est en constante croissance, avec un pic important vers les années 60, qu'on peut peut-être associer à l'augmentation de la fréquentation des plages ou au développement de l'industrie de la pêche. On peut aussi supposer que des campagnes de sensibilisation et des réglementations mises en place sont responsables de la chute de ce pic. L'augmentation importante depuis les années 90 est probablement due aux mêmes facteurs, on doit cependant nuancer cela avec le fait qu'avec l'arrivée d'internet et la démocratisation du téléphone portable, il est bien plus facile de signaler les incidents.

#### "Gender"
Sur le deuxième graphique, on remarque que la grande majorité des victimes d'attaques de requin (80%) sont des hommes. 

#### "Not fatal attack"
Pour le troisième graphique, qui consiste de deux bar graphs, on peut observer les attaques.
Lorsque l’on choisit ‘fatal attack’, on observe le nombre d’attaque fatale(qui induit le décès de la personne) en fonction de l’espèce de requin : on remarque que le requin tigre est le plus meurtrier. Si on choisit ‘not fatal attack’, on observe le nombre d’attaque non fatale(qui induit au maximum une blessure) en fonction de l’espèce de requin : on voit beaucoup de requins entre 1 et 2 mètres de long (la taille assez globale de requin), mais l’espèce de requin n’est pas spécifiée. L’espèce de requin connue qui attaque le plus est aussi le requin tigre.

#### "Activity"
Sur ce graphique, un bar graph, on peut observer quelles étaient les activités pratiquées par les victimes lors de chaque attaque, lorsque c'est renseigné. Sans surprise, c'est la pêche qui est responsable d'une écrasante majorité des attaques.

#### "Shark attack map"
Ce graphique permet de représenter sur une carte du monde les différentes attaques de requins par pays à travers le monde. On peut alors observer que la plupart des attaques de requins sont subies dans trois pays, à savoir les États-Unis, l'Australie et l'Afrique du Sud. 
On peut aussi observer que la quasi-totalité des pays bordant une mer ou un océan ont subi au moins une attaque.
Il y a sur cet onglet un menu déroulant permettant de naviguer entre la carte du monde et celles des États-Unis, de l'Australie et de l'Afrique du Sud, et sur chacune d'entre elles, on observe que les attaques sont généralement concentrées sur quelques États/Département à éviter. On notera particulièrement que la Floride, aux États-Unis, subit près de 20% des attaques recensées (~18,6%).

#### "Time"
Il y a deux graphiques sur la temporalité des attaques. Le premier est un histogramme montrant le nombre d’attaque par heure, avec un pic à 11h mais le taux est aussi élevé durant l’après-midi. Cela se traduit peut-être par le fait que c’est à ces heures-là que les personnes sortent le plus en mer, et non à ces heures-là que les requins attaquent le plus. Le deuxième graphique est un camembert qui appuie ces observations plus visuellement, avec plus de 50% des attaques se déroulant durant l’après-midi. 

#### "Attacks by age"

Ce dernier graphique est un histogramme montrant les attaques selon l’âge des victimes. Il y a une checkbox qui, appuyée permet de montrer les détails de si ces attaques ont été meurtrières ou non. 

#### "Conclusion"
dzf

## Developer Guide

Nous observerons ici la structuration du projet.
Pour expliquer le fonctionnement de ce projet, nous suivrons la manipulation des données faite dans `main.py`. 
Mais tout d'abord, nous devons télécharger les données avec le fichier `get_data.py`.
Pour les besoins du projets, nous utilisons la library **opendatasets** pour récupérer le jeu de données. Étant donné que nous récupérons les données sur kaggle, un token personnel est nécessaire. Nous sommes conscients que c'est une pratique à éviter, mais le projet étant publié uniquement sur le Git de l'ESIEE les risques sont assez faibles. Le token sera tout de même supprimé du Git après l'évaluation du projet. Il aurait été possible de télécharger le dataset et de le mettre directement dans le Git, mais après concertation en cours, nous avons convenu que l'approche du token était préférable.
Dans `get_data.py` donc, nous spécifions l'adresse url du dataset que nous souhaitons sélectionner, puis nous le téléchargeons dans le sous-dossier `ressources`. Notons que s'il est possible de changer l'adresse url afin de télécharger un jeu de donnée différent, toutes les autres fonctions sont adaptées pour ce jeu de données spécifique et le programme ne fonctionnera donc pas.

#### data_processing.py

C'est dans ce fichier que se trouvent les fonctions servant à modifier, nettoyer, arranger le dataset.
On y trouve donc les fonctions :
- get_data() : Permet de vérifier le téléchargement du jeu de donnée et retourne un dataframe.
- filtration_df(df) : Permet de nettoyer la majeure partie du dataset.
- clean_time(df) : Permet de normaliser la colonne [Time].
- categorize_time(df) : Permet de catégoriser les heures en 4 périodes de temps : Morning, Afternoon, Evening et Night, ce qui servira pour un graphique.

#### graphs .py
C'est ici que sont construits la plupart des graphiques, à savoir tous ceux qui ne contiennent pas de carte. Les figures sont créés en utilisant la library **plotly.express** On aura ici donc les fonctions suivantes :
-  byYearGraph(df)
-  byActivityGraph(df)
-  bySexGraph(df)
-  hoursGraph(df)
-  periodGraph(df)
-  ageGraph(df)

Chaque fonction prend en paramètre le dataframe correspondant aux données analysées, et renvoie une figure.

#### maps .py
Ce fichier fonctionne de façon similaire au précédent, mais il permet de créer les figures avec une carte. On aura donc : 
- worlGraph(df) : Carte du monde avec les attaques par pays.
- usaGraph(df) : Carte des États-Unis avec les attaques par état.
- australiaGraph(df) : Carte de l'Australie avec les attaques par état.
- africaGraph(df) : Carte de l'Afrique du Sud avec les attaques par province.

On utilisera ici aussi la library **plotly.express** afin de créer nos figures. 
Dans cette library, la carte du monde et la carte des États-Unis sont déjà préconstruites, on peut donc les spécifier directement dans le paramètre **locationmode** de la fonction **choropleth** que l'on utilise pour créer nos figures.
Pour la carte de l'Australie et celle de l'Afrique du Sud, nous avons eu besoin de prendre des cartes disponibles sur Internet :
- https://github.com/rowanhogan/australian-states/blob/master/states.geojson pour la carte de l'Australie.
- https://github.com/fletchjeff/ZA-Census-Data-Explorer/blob/main/assets/za-provinces.topojson pour la carte de l'Afrique du Sud, fichier en .topojson que l'on a converti en .json à l'aide d'un site.

Ces deux fichiers se trouvent dans le sous-dossier **ressources**.

#### dashboard .py

Ce fichier n'est constitué que d'une seule fonction **create_dashboard** qui permet de mettre en place le dashboard et qui est constitué de plusieurs paramètres : 
- app : Le dashboard déjà existant que l'on va modifier.
- fig_year, fig_sx, fig_activity, fig_world, fig_hours, fig_time_periods et fig_age : Les figures qui seront mises en place à l'état initial du dashboard.

#### callbacks .py

De même, ce fichier n'est constitué que d'une seule fonction **get_callbacks** qui permet d'ajouter les callbacks au dashboard. Les paramètres sont :
- app : Le dashboard auquel on va ajouter les différents callbacks 
- shark_sorted_df : Un dataframe créé lors de la création de la figure **ageGraph**  que l'on réutilise pour créer d'autres figures.
- sharks_species, fig_age, fig_usa, fig_aus, fig_sa, fig_world : Les figures à afficher en fonction des différents paramètres sélectionnés sur le dashboard.

#### main .py

 Ce fichier permet de lancer le dashboard. Pour ce faire, la fonction **main** permet tout d'abord d'instancier le dashboard, ici **app**, et d'associer le dataframe créé à partir du jeu de donnée à une variable, ici **shark_data**, à l'aide de la fonction **get_data()** du fichier `data_processing.py`. Remarquons que si les données n'ont pas été téléchargées, le programme s'arrête et un message d'erreur s'affiche, indiquant le motif du problème et modifiable dans la fonction précédement citée.
Ensuite, la fonction permet d'instancier chaque figure et de les associer à une variable différente, puis appelle la fonction **create_dashboard** qui va mettre en place le dashboard. L'appel de la fonction **get_callbacks** permet d'ajouter les callbacks nécéssaire.
Enfin, on appelle la fonction **run_server** sur notre dashboard **app** afin de lancer le dashboard sur un serveur local.

#### Modifier/Ajouter du code

Pour modifier une figure, il suffit d'aller dans le fichier où elle se trouve (`maps.py` ou `graphs.py`) et la modifier directement. 
Pour ajouter une figure, il faut, si besoin, créer une fonction de tri/nettoyage dans `data_processing.py`, puis selon si elle contient une carte ou non la créer dans `maps.py` ou `graphs.py`. Pour l'afficher, il faudra :
- Si elle doit apparaitre lors de l'initialisation du dashboard, l'ajouter comme paramètre dans la fonction **create_dashboard** que l'on modifiera dans le fichier `dashboard.py`. Dans cette fonction, vous pouvez créer de nouveaux onglets pour afficher de nouvelles figures, ou l'ajouter à la suite d'autres figures dans des onglets déjà existants.
- Si elle doit apparaitre lors de l'appel de certains callbacks, l'ajouter comme paramètre dans la fonction **get_callbacks** que l'on modifiera dans le fichier `callbacks.py`. Ici, on pourra définir lors de quels appels cette figure doit être affichée. Il faudra tout de même modifier le dashboard dans `dashboard.py` pour créer les appels et/ou définir où cette figure sera affichée

Enfin, il faudra l'instancier dans la fonction **main** du fichier `main.py` avant l'appel de **create_dashboard** ou **get_callbacks** et l'ajouter en paramètre à l'une de ces deux fonctions selon le cas.
