import scrapy
from pymongo import MongoClient
import re


class Esf2Spider(scrapy.Spider):
    name = "esf2"
    allowed_domains = []

    def start_requests(self):
        base_url = "https://technique.clubesf.com/resultat/ajax_classement_load.php"
        query_params = {
            'categ': '',
            'sexe': '',
            'an_inf': '',
            'an_sup': '',
            'point_inf': '',
            'point_sup': '',
            'nation': '',
            'cp': '',
            'nom': '',
            'prenom': '',
            'page': '25',
            'index': 0,  # Ce paramètre sera incrémenté
            'page': '5000',
            'total': '105922',
            '_': '1706021334267'
        }

        index_max = 65000  # Sur le site, on peut voir qu'il y a uniquement 69000 skieurs classé. On pourrais récuperer ce nombre automatiquement, mais ce n'est pas très important ici.
        step = 5000

        for index in range(0, index_max + 1, step):
            query_params['index'] = str(index)
            url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        noms = [nom.get() for nom in response.css("a::text")[1::2]]
        codes = [code.get() for code in response.css("a::text")[0::2]]
        sexes = response.css('tbody tr td:nth-child(3)::text').getall()
        pays = response.css('tr > td:nth-child(5)::text').getall()
        points = response.css('tr > td:nth-child(7)::text').getall()

        categories = []

        for tr in response.css('table.table-striped > tbody > tr'):
            # On essaye de récupérer la categorie, s'il n'y en a pas, on met une chaîne vide
            categorie = tr.css('td:nth-child(4)::text').get(default='').strip()
            categories.append(categorie)

        departements = []
        for tr in response.css('table.table-striped > tbody > tr'):
            # On essaye de récupérer du département, s'il n'y en a pas, on met une chaîne vide
            departement_text = tr.css('td:nth-child(6)::text').get(default='').strip()
            # On utilise une expression régulière pour vérifier si c'est un nombre
            if re.match(r'^\d+$', departement_text):
                departements.append(departement_text)
            else:
                # Si ce n'est pas un nombre, on ajoute une chaîne vide
                departements.append('')

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
        client = MongoClient('mongodb', 27017)
        db = client['esf']
        collection = db['skieurs']

        for i in range(0, len(noms)):
            document = {
                'ID': codes[i],
                'Nom': noms[i],
                 #'Sexe': sexes[i],
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