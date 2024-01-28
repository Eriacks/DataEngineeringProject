import scrapy
from pymongo import MongoClient


class Esf1Spider(scrapy.Spider):
    name = "esf1"
    allowed_domains = []
    start_urls = ["https://www.esf.net/ecole-de-ski/"]


    def parse(self, response):
        urls = []
        for i in range(1, 213):
            # les infos sur les ecoles
            a_tag = response.css(f'a.sg-list-ecoles__item:nth-child({i})')

            # Extraire les parties d'URL pour chaque ecole
            url = a_tag.css('::attr(href)').get()
            url = url.replace('/ecole-de-ski/', '')
            url = response.urljoin(url)
            urls.append(url)

            for new_url in urls:
                yield scrapy.Request(url=new_url, callback=self.parse_new_url)

    def parse_new_url(self, response):
        nom_ecole = response.css('span.title-1__inner__main::text').getall()[1]

        nombre_instructeur = response.css(
'.sg-infobox-colored__item--red .sg-infobox-colored__item__number::text').get()

        nombre_instructeur_parlant_anglais = response.css(
'.sg-infobox-colored__item__number .rich-text__inner::text').get()

        station_info = response.css('.sg-txt-bigimage__txt li b::text').getall()
        station_info = [element.strip() for element in station_info if element.strip()]
        station_info = [f"{station_info[i]} {station_info[i + 1]}" for i in
                                    range(0, len(station_info), 2)]

        avantages = response.css('.sg-imgtxt-bloc__txt ul li b::text').getall()
        avantages = [element.strip() for element in avantages if element.strip()]

        disciplines= response.css('a.sg-radimg-link__link h3.sg-radimg-link__title::text').getall()
        disciplines = [element.strip() for element in disciplines if element.strip()]


        address_elements = response.xpath('//div[@class="sg-txt-bigimage__txt"]/text()').getall()
        address_elements = [element.strip() for element in address_elements if element.strip()]
        address = ' '.join(address_elements)

        phone = response.css('.shcool-phone b::text').get()

        document = {
            'Nom': nom_ecole,
            'Nombre de moniteurs': nombre_instructeur,
            'Nombre de moniteurs parlant anglais': nombre_instructeur_parlant_anglais,
            'Informations de la station': station_info,
            'Avantages de l\'école': avantages,
            'Disciplines': disciplines,
            'Adresse': address,
            'Tel': phone
        }

        # Insertion du document dans la collection MongoDB
        client = MongoClient('localhost', 27017)
        db = client['esf']
        collection = db['ecoles']
        collection.insert_one(document)

