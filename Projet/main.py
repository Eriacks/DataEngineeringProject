import subprocess
import os
from flask import Flask

import dash
from dash import dcc, html
import re
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from ast import literal_eval

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['esf']
collection = db['ecoles']


def getNumbers(s):
    # Extract all numbers from the string and return as a list
    return [int(num) for num in re.findall(r'\d+', str(s))]


def dataFrame_infoStation():
    # Récupération des données depuis MongoDB
    cursor = collection.find({}, {'_id': 0,  'Informations de la station': 1})
    data = list(cursor)

    # Création d'un DataFrame
    return  pd.DataFrame(data)

def dataFrame_adresse():
    # Récupération des données depuis MongoDB
    cursor = collection.find({}, {'_id': 0, 'Nom': 1, 'Adresse': 1})
    data = list(cursor)

    # Création d'un DataFrame
    return  pd.DataFrame(data)

def dataFrame_moniteurs():
    # Récupération des données depuis MongoDB
    cursor = collection.find({}, {'_id': 0, 'Nombre de moniteurs': 1, 'Nombre de moniteurs parlant anglais':1})
    data = list(cursor)
    df = pd.DataFrame(data)
    df['Nombre de moniteurs'] = pd.to_numeric(df['Nombre de moniteurs'], errors='coerce')
    df['Nombre de moniteurs parlant anglais'] = df['Nombre de moniteurs parlant anglais'].fillna(0)
    df['Nombre de moniteurs parlant anglais'] = pd.to_numeric(df['Nombre de moniteurs parlant anglais'], errors='coerce')
    # Création d'un DataFrame
    return df

def create_histo_km_piste(df):
    # Évaluer la liste 'Informations de la station' pour extraire le nombre de kilomètres de piste
    df['km_piste'] = df['Informations de la station'].apply(lambda x: getNumbers(x)[0] if x else None)
    df['km_piste'] = df['km_piste'].fillna(0)
    # Convertir la colonne 'km_piste' en type numérique
    df['km_piste'] = pd.to_numeric(df['km_piste'], errors='coerce')

    fig = px.histogram(df, x='km_piste', nbins=20,
                       title="Histogramme du Nombre de Kilomètres de Piste",
                       labels={'km_piste': "Nombre de Kilomètres de Piste", 'count': 'Fréquence'},
                       color_discrete_sequence=['blue'])

    # Affichage de l'histogramme
    return fig

def create_histo_snowparks(df):
    # Évaluer la liste 'Informations de la station' pour extraire le nombre de kilomètres de piste
    df['snowparks'] = df['Informations de la station'].apply(lambda x: getNumbers(x)[2] if len(getNumbers(x)) >= 3 else None)
    df['snowparks'] = df['snowparks'].fillna(0)
    # Convertir la colonne 'km_piste' en type numérique
    df['snowparks'] = pd.to_numeric(df['snowparks'], errors='coerce')

    fig = px.histogram(df, x='snowparks', nbins=20,
                       title="Histogramme du Nombre de Snowparks",
                       labels={'snowparks': "Nombre de Snowparks", 'count': 'Fréquence'},
                       color_discrete_sequence=['blue'])

    return fig

def create_histo_remonte(df):
    # Évaluer la liste 'Informations de la station' pour extraire le nombre de kilomètres de piste
    df['remonte'] = df['Informations de la station'].apply(lambda x: getNumbers(x)[1] if len(getNumbers(x)) >= 2 else None)
    df['remonte'] = df['remonte'].fillna(0)
    # Convertir la colonne 'km_piste' en type numérique
    df['remonte'] = pd.to_numeric(df['remonte'], errors='coerce')

    fig = px.histogram(df, x='remonte', nbins=20,
                       title="Histogramme du Nombre de remontées mécaniques",
                       labels={'remonte': "Nombre de remontées mécaniques", 'count': 'Fréquence'},
                       color_discrete_sequence=['blue'])

    return fig


def create_histo_moni(df):
    # Création de l'histogramme avec Plotly Express
    fig = px.histogram(df, x='Nombre de moniteurs', nbins=20,
                       title="Histogramme du Nombre de Moniteurs",
                       labels={'Nombre de moniteurs': "Nombre de Moniteurs", 'count': 'Fréquence'},
                       color_discrete_sequence=['skyblue'])

    return fig

def create_histo_moni_anglais(df):
    fig = px.histogram(df, x='Nombre de moniteurs parlant anglais', nbins=20,
                       title='Histogramme du Nombre de Moniteurs parlant anglais',
                       labels={'Nombre de moniteurs parlant anglais': 'Nombre de Moniteurs',
                               'count': 'Fréquence'})
    return fig

# Fonction pour obtenir les coordonnées (latitude, longitude) d'une adresse
def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None  # Retourne None si les coordonnées ne peuvent pas être trouvées

def map():
    df = dataFrame_adresse()
    df['Latitude'], df['Longitude'] = zip(*df['Adresse'].apply(get_coordinates))
    print(df.isna().sum())

def run_scrapy_spider():
    spider_path = os.path.abspath("esf/esf/spiders")
    command = f"cd {spider_path} && scrapy runspider esf1.py"

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de l'araignée Scrapy : {e}")



# Initialiser l'application Dash
app = dash.Dash(__name__)

df_moni = dataFrame_moniteurs()
df_info = dataFrame_infoStation()

# Create the Dash app
app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H2('Sidebar'),
        dcc.Link('Ecoles', href='/ecoles'),
        html.Br(),  # Add a line break
        dcc.Link('Classement', href='/classement')
    ], style={'width': '20%', 'position': 'fixed', 'height': '100%', 'backgroundColor': '#f8f9fa'}),

    # Main content
    html.Div([
        # Your main content goes here
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ], style={'marginLeft': '20%', 'padding': '20px'}),

    # Tabs for Ecoles page
    dcc.Tabs(
        id='ecoles-tabs',
        value='tab-1',
        children=[
            dcc.Tab(label='Tab 1', value='tab-1'),
            dcc.Tab(label='Tab 2', value='tab-2'),
        ]
    ),
    # Tab content for Ecoles page
    html.Div(id='ecoles-tabs-content')
])

# Callback to update the page content and tab content based on the URL and selected tab
@app.callback(
    [dash.dependencies.Output('page-content', 'children'),
     dash.dependencies.Output('ecoles-tabs-content', 'children')],
    [dash.dependencies.Input('url', 'pathname'),
     dash.dependencies.Input('ecoles-tabs', 'value')]
)
def display_content(pathname, selected_tab):
    if pathname == '/ecoles':
        # Tab content for Ecoles page
        tab_content = update_ecoles_tab(selected_tab)
        return html.Div(tab_content), tab_content
    elif pathname == '/classement':
        return html.H1('Classement Page'), None
    else:
        return html.H1('Home Page'), None

# Function to update the tab content based on the selected tab
def update_ecoles_tab(selected_tab):
    if selected_tab == 'tab-1':
        # Replace with your graph 1 component
        return dcc.Graph(figure=create_histo_moni(df_moni))
    elif selected_tab == 'tab-2':
        # Replace with your graph 2 component
        return dcc.Graph(figure=create_histo_snowparks(df_info))
    else:
        return html.H1('Invalid Tab')

if __name__ == "__main__":
    #run_scrapy_spider()
    app.run_server(debug=True)




