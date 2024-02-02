# Les ecoles de ski et le classement des skieurs

## Introduction

Cette étude analyse les données relatives aux écoles de ski et au classement des skieurs. Les ensembles de données sont extraits du site esf.net. Nous avons choisi de travailler sur 2 choses différentes du même site, donc nous aurons des informations sur le classement des skieurs et les différentes écoles de ski.

Les données extraites sur les écoles de ski sont les suivantes :

Nom: Nom de l'école de ski.
Nombre de moniteurs: Nombre total de moniteurs dans l'école.
Nombre de moniteurs parlant anglais: Nombre de moniteurs parlant anglais dans l'école.
Informations de la station: Informations sur la station de ski associée à l'école.
Avantages de l'école: Avantages spécifiques de l'école.
Disciplines: Disciplines enseignées par l'école.
Adresse: Adresse physique de l'école.
Téléphone: Numéro de téléphone de l'école.

Les données extraites sur les classements des skieurs sont les suivantes :

ID: Identifiant du skieur.
Nom: Nom du skieur.
Sexe: Sexe du skieur.
Catégorie: Catégorie à laquelle appartient le skieur.
Nationalité: Nationalité du skieur.
Département: Département associé au skieur.
Point: Nombre de points du skieur.
Classement global: Classement général du skieur.
Classement dans la catégorie: Classement du skieur dans sa catégorie.
Classement national: Classement national du skieur.
Classement départemental: Classement départemental du skieur.


## User Guide

Pour visualiser les données et voir le dashboard final, il vous faudra tout d'abord cloner le dépôt Git sur sa machine. Pour cela, vous pouvez vous placer dans le dossier souhaité à l'aide de la commande :
```sh
$ cd /chemin/vers/votre/répertoire/de/projets
```
Puis cloner le dépôt Git avec la commande : 
```sh
$ git clone https://github.com/Eriacks/DataEngineeringProject
```
En cas de problème, vérifiez que vous êtes bien connecté avec vos identifiants Git.
A présent, si vous regardez votre dossier, vous devriez y trouver une copie complète du dépôt Git.

Vous devez alors lancer le docker compose avec la commande, tout en étant dans le répertoire ou se situe le fichier .yml
```sh
$ docker compose up
```
Cela lancera les différentes étapes du projet

Et vous pourrez y aux adresses suivantes : 
```sh
http://0.0.0.0:8050/
http://localhost:8050/
```
Pour stopper les applications, vous pouvez utiliser les commandes `docker stop id_image` dans n'importe quel terminal. l'id image peut être récupérer avec la commande `docker ps`. 
Si cela ne fonctionne pas la première fois, il y a peut-être eu une erreur du au fait que l'application dashboard a été lancée avant les spiders, si c'est le cas, il faudra relancer la commande `docker compose up` mais arrêter le docker pour ne pas qu'il refasse le scrapping avec controle + C.


##  Rapport d’analyse


## Developer Guide
Notre projet est composé de plusieurs dossiers : dash_app, scrapy_project1 et scrapy_project2 ainsi qu'un fichier docker-compose.

#### docker-compose.yml
Ce fichier comporte les lignes nécessaires pour lancer les différentes applications. Avec la commande docker compose up, le fichier s'executera.
D'abord un docker mongo se lancera, pour accueillir les données scrapées. Ensuite le scrapping des écoles se lancera, mettra les données dans la base de donnée mongo, puis vient le scrapping des classements et enfin l'application dash se lancera.

#### scrapy_project
Ce dossier comporte un dockerfile, qui s'occupe de lancer le scrapping sur un docker. Il intègre les requirements nécessaire au scrapping que le dockerfile s'occupe d'installer. Il comporte aussi la spider esf.py qui s'occupera du scrapping des ecoles des ski.

#### scrapy_project2
Ce dossier comporte un dockerfile, qui s'occupe de lancer le scrapping sur un docker. Il intègre les requirements nécessaire au scrapping que le dockerfile s'occupe d'installer. Il comporte aussi la spider esf.py qui s'occupera du scrapping des classements de ski.

#### dash_app
Ce dossier comporte un dockerfile, qui s'occupera de lancer l'application dash sur un docker. Il intègre les requirements nécessaire au dashboard et aux graphiques que le dockerfile s'occupe d'installer. Il comporte aussi les fichiers python nécessaires à sa création : main.py qui crée le dashboard ainsi que graphs.py qui crée les dataframe et les graphiques.
