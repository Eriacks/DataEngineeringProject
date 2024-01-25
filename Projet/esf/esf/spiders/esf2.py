import scrapy
from pymongo import MongoClient


class Esf2Spider(scrapy.Spider):
    name = "esf2"
    allowed_domains = []
    start_urls = ["https://technique.clubesf.com/resultat/ajax_classement_load.php?categ=&sexe=&an_inf=&an_sup=&point_inf=&point_sup=&nation=&cp=&nom=&prenom=&page=25&index=0&page=5000&total=105922&_=1706021334267"]

    def parse(self, response):

        noms = [nom.get() for nom in response.css("a::text")[1::2]]
        codes = [code.get() for code in response.css("a::text")[0::2]]
        sexes = response.css('tbody tr td:nth-child(3)::text').getall()
        pays = response.css('tr > td:nth-child(5)::text').getall()
        points = response.css('tr > td:nth-child(7)::text').getall()
        
        
        categories = []
        
        for tr in response.css('table.table-striped > tbody > tr'):
            # On essaye de récupérer le texte du département, s'il n'y en a pas, on met une chaîne vide
            categorie = tr.css('td:nth-child(4)::text').get(default='').strip()
            categories.append(categorie)
            
        
        departements = []
        for tr in response.css('table.table-striped > tbody > tr'):
            # On essaye de récupérer le texte du département, s'il n'y en a pas, on met une chaîne vide
            departement = tr.css('td:nth-child(6)::text').get(default='').strip()
            departements.append(departement)

        
        classement_global = []
        classement_categorie = []
        classement_nation = []
        classement_departement = []
        compteur = 0

        for td in response.css('td.text-right'):
            classement_value = td.css('span::text').get()

            compteur += 1
            
            if compteur == 2:
                classement_global.append(classement_value)
            elif compteur == 3:
                classement_categorie.append(classement_value)
            elif compteur == 4:
                classement_nation.append(classement_value)
            elif compteur == 5:
                classement_departement.append(classement_value)
                compteur = 0
             
  
             
        # Insertion du document dans la collection MongoDB
        client = MongoClient('localhost', 27017)
        db = client['esf']
        collection = db['skieurs']         

        for i in range (0,len(noms)):
            document = {
                'ID' : codes[i],
                'Nom': noms[i],
                'Sexe': sexes[i],
                'Catégorie': categories[i],
                'Nationalité': pays[i],
                'Département': departements[i],
                'Point': points[i],
                'Classement global': classement_global[i],
                'Classement dans la catégorie': classement_categorie[i],
                'Classement national': classement_nation[i],
                'Classement departemental': classement_departement[i],
            }
            collection.insert_one(document)
