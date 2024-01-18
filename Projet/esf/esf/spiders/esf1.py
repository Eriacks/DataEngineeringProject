import scrapy
import re
from pymongo import MongoClient

class Esf1Spider(scrapy.Spider):
    name = "esf1"
    allowed_domains = ["www.esf.net"]
    start_urls = ["https://technique.esf.net/resultat/classement.php"]

    def parse(self, response):

        client = MongoClient()
        db = client["esf"]
        collection = db["classement_ski_open"]
        # Utilisez response.css pour sélectionner la balise <tbody>
        tbody = response.css('table > tbody')

        # Sélectionnez toutes les lignes de la balise <tbody>
        lignes = tbody.css('tr')

        for ligne in lignes:
            # Extractez le nom
            nom = ligne.css('td:nth-child(2) a::text').get()

            # Extractez les caractéristiques
            code = ligne.css('td:nth-child(1) a::text').get()
            sexe = ligne.css('td:nth-child(3)::text').get()
            categorie = ligne.css('td:nth-child(4)::text').get()
            nationalite = ligne.css('td:nth-child(5)::text').get()
            département = ligne.css('td:nth-child(6)::text').get()
            points = ligne.css('td:nth-child(7)::text').get()

            classement_info = ligne.css('td:nth-child(8)').extract_first()
            l = self.extract_numbers_from_string(classement_info)
            classement_info = f"{str(l[0])}/{str(l[1])}"

            classement_categorie = ligne.css('td:nth-child(9)').extract_first()
            l = self.extract_numbers_from_string(classement_categorie)
            classement_categorie = f"{str(l[0])}/{str(l[1])}"

            nation = ligne.css('td:nth-child(10)').extract_first()
            l = self.extract_numbers_from_string(nation)
            nation = f"{str(l[0])}"

            dpt = ligne.css('td:nth-child(11)').extract_first()
            l = self.extract_numbers_from_string(dpt)
            dpt = f"{str(l[0])}"

            # Imprimez ou stockez les informations extraites
            print('Nom:', nom)
            print('Code:', code)
            print('Sexe:', sexe)
            print('Catégorie:', categorie)
            print('Nationalité:', nationalite)
            print('Points:', points)
            print('Département:', département)
            print('Classement Général:', classement_info)
            print('Classement Catégorie:', classement_categorie)
            print('Classement Nation:', nation)
            print('Classement Département:', dpt)
            print('---')
            # Créez un dictionnaire avec les données extraites
            item = {
                "nom": nom,
                "code": code,
                "sexe": sexe,
                "categorie": categorie,
                "nationalite": nationalite,
                "departement": département,
                "points": points,
                "classement_info": classement_info,
                "classement_categorie": classement_categorie,
                "Classement Nation": nation,
                "Classement Département": dpt
            }

            # Insérez le dictionnaire dans la base de données MongoDB
            collection.insert_one(item)

    def extract_numbers_from_string(self, s):
        return [int(x) for x in re.findall(r'\b\d+\b', s)]
