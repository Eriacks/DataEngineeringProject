import plotly.express as px
import json
import pandas as pd
from bson.decimal128 import Decimal128
import re
from pymongo import MongoClient

# se connecter a la db
client = MongoClient('mongodb', 27017)
db = client['esf']
collection = db['ecoles']
collection_skieurs = db['skieurs']


def create_choropleth_map(collection):
    with open('france.geojson', 'r') as file:
        fr_map = json.load(file)  # https://france-geojson.gregoiredavid.fr/repo/departements.geojson

    pipeline = [
        {"$group": {"_id": "$Département", "Count": {"$sum": 1}}},  # Grouper par région et compter
    ]

    resultats = list(collection.aggregate(pipeline))  # Exécuter la pipeline d'agrégation

    region_counts = [{'Area': resultat['_id'], 'Count': resultat['Count']} for resultat in
                     resultats]  # Créer un dictionnaire pour les régions avec les comptes
    region_counts = [item for item in region_counts if item['Area'] != '']

    # Vérifier si chaque région est présente dans region_counts, sinon l'ajouter avec un Count de 0
    all_regions = [f"{i:02d}" for i in range(1, 96)]
    for region_code in all_regions:
        if not any(region['Area'] == region_code for region in region_counts):
            region_counts.append({'Area': region_code, 'Count': 0})

    # Convertir region_counts en DataFrame Pandas
    df_region_counts = pd.DataFrame(region_counts)

    # Assurez-vous que la colonne 'Area' est de type string
    df_region_counts['Area'] = df_region_counts['Area'].astype(str)

    region_names = {feature['properties']['code']: feature['properties']['nom']
                    for feature in fr_map['features']}
    df_region_counts['Nom_region'] = df_region_counts['Area'].map(region_names)

    # Créer la figure choroplèthe
    fig = px.choropleth(
        df_region_counts,
        geojson=fr_map,
        locations='Area',  # Nom de la colonne dans DataFrame qui fait référence aux codes des régions
        color='Count',
        hover_data=['Nom_region'],
        # color_continuous_scale="Viridis",
        featureidkey="properties.code",
        title='Distribution des skieurs par région'
    )

    # Mise à jour de la mise en page de la figure
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 10})
    fig.update_geos(fitbounds="locations", visible=False)

    # Retourner la figure
    return fig


def average_ranking_histogram(collection):
    result = collection.aggregate([{"$addFields": {"Classement global": {"$toDecimal": "$Classement global"}}},
                                   {"$group": {"_id": "$Catégorie", "average": {"$avg": "$Classement global"}}}])
    result_list = list(result)

    df = pd.DataFrame(result_list)
    df.rename(columns={'_id': 'Category', 'average': 'Average Ranking'}, inplace=True)
    df['Average Ranking'] = df['Average Ranking'].apply(
        lambda x: float(x.to_decimal()) if isinstance(x, Decimal128) else x)
    df['Category'] = df['Category'].replace({'SH': 'Seniors', 'SD': 'Seniors', 'VH': 'Masters',
                                             'VD': 'Masters'})  # On remplace les catégories SH et SD par Seniors, et VH et VD par Masters (On ne différencie pas les sexes)

    # Regrouper par la nouvelle catégorie et recalculer la moyenne
    df = df.groupby('Category')['Average Ranking'].mean().reset_index()
    df['Average Ranking'] = df['Average Ranking'].round()
    category_order = ['U8', 'U10', 'U12', 'U14', 'U16', 'U18', 'U21', 'Seniors', 'Masters']

    df['Category'] = pd.Categorical(df['Category'], categories=category_order, ordered=True)
    df.sort_values('Category', inplace=True)

    # Create the bar chart
    fig = px.bar(df, x='Category', y='Average Ranking', title='Classement moyen par catégorie')

    fig.update_traces(
        texttemplate='%{y:.0f}',  # On affiche les nombres entiers
        hovertemplate='<b>Catégorie:</b> %{x}<br><b>Classement moyen:</b> %{y:.0s}<extra></extra>'
    )

    fig.update_layout(
        yaxis_title='Classement moyen',
        xaxis_title='Catégorie',
        plot_bgcolor='rgba(252,248,244,1.00)',
        paper_bgcolor='cornsilk',
        font=dict(family="Montserrat", size=18, color='black')
    )

    # Retourne la figure
    return fig


def create_histo_remonte(df):
    # Évaluer la liste 'Informations de la station' pour extraire le nombre de remontées mécaniques
    df['remonte'] = df['Informations de la station'].apply(
        lambda x: getNumbers(x)[1] if len(getNumbers(x)) >= 2 else None)

    # gérer les NA potentiels
    df['remonte'] = df['remonte'].fillna(0)

    # Convertir la colonne 'km_piste' en type numérique
    df['remonte'] = pd.to_numeric(df['remonte'], errors='coerce')

    # création de la figure
    fig = px.histogram(df, x='remonte', nbins=50,
                       title="Histogramme du Nombre de remontées mécaniques",
                       labels={'remonte': "Nombre de remontées mécaniques", 'count': 'Fréquence'},
                       color_discrete_sequence=['skyblue'])
    # Retourne la figure
    return fig


def create_histo_moni(df):
    # Création de l'histogramme
    fig = px.histogram(df, x='Nombre de moniteurs', nbins=50,
                       title="Histogramme du Nombre de Moniteurs",
                       labels={'Nombre de moniteurs': "Nombre de Moniteurs", 'count': 'Fréquence'},
                       color_discrete_sequence=['skyblue'])
    # Retourne la figure
    return fig


def create_histo_moni_anglais(df):
    # Création de l'histogramme
    fig = px.histogram(df, x='Nombre de moniteurs parlant anglais', nbins=50,
                       title='Histogramme du Nombre de Moniteurs parlant anglais',
                       labels={'Nombre de moniteurs parlant anglais': 'Nombre de Moniteurs', 'count': 'Fréquence'},
                       color_discrete_sequence=['red  '])
    # Retourne la figure
    return fig


def create_histo_snowparks(df):
    # Évaluer la liste 'Informations de la station' pour extraire le nombre de snowparks
    df['snowparks'] = df['Informations de la station'].apply(
        lambda x: getNumbers(x)[2] if len(getNumbers(x)) >= 3 else None)
    # gérer les NA potentiels
    df['snowparks'] = df['snowparks'].fillna(0)
    # Convertir la colonne 'km_piste' en type numérique
    df['snowparks'] = pd.to_numeric(df['snowparks'], errors='coerce')

    # Création de l'histogramme
    fig = px.histogram(df, x='snowparks', nbins=20,
                       title="Histogramme du Nombre de Snowparks",
                       labels={'snowparks': "Nombre de Snowparks", 'count': 'Fréquence'},
                       color_discrete_sequence=['skyblue'])
    # Retourne la figure
    return fig


def getNumbers(s):
    # extraire seulement les nombres d'une string
    return [int(num) for num in re.findall(r'\d+', str(s))]


def create_histo_km_piste(df):
    # Évaluer la liste 'Informations de la station' pour extraire le nombre de kilomètres de piste
    df['km_piste'] = df['Informations de la station'].apply(lambda x: getNumbers(x)[0] if x else None)
    # gérer les NA potentiels
    df['km_piste'] = df['km_piste'].fillna(0)
    # Convertir la colonne 'km_piste' en type numérique
    df['km_piste'] = pd.to_numeric(df['km_piste'], errors='coerce')
    # Création de l'histogramme
    fig = px.histogram(df, x='km_piste', nbins=50,
                       title="Histogramme du Nombre de Kilomètres de Piste",
                       labels={'km_piste': "Nombre de Kilomètres de Piste", 'count': 'Fréquence'},
                       color_discrete_sequence=['skyblue'])

    # Affichage de l'histogramme
    return fig


def dataFrame_infoStation():
    # Récupération des données depuis MongoDB
    cursor = collection.find({}, {'_id': 0, 'Informations de la station': 1})
    data = list(cursor)
    # Création d'un DataFrame
    return pd.DataFrame(data)


def dataFrame_moniteurs():
    # Récupération des données depuis MongoDB
    cursor = collection.find({}, {'_id': 0, 'Nombre de moniteurs': 1, 'Nombre de moniteurs parlant anglais': 1})
    data = list(cursor)
    df = pd.DataFrame(data)
    df['Nombre de moniteurs'] = pd.to_numeric(df['Nombre de moniteurs'], errors='coerce')
    # gérer les NA potentiels
    df['Nombre de moniteurs parlant anglais'] = df['Nombre de moniteurs parlant anglais'].fillna(0)
    # mettre en numérique
    df['Nombre de moniteurs parlant anglais'] = pd.to_numeric(df['Nombre de moniteurs parlant anglais'],
                                                              errors='coerce')
    # Création d'un DataFrame
    return df


