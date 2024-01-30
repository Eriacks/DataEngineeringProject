import plotly.express as px
import json
import pandas as pd
from bson.decimal128 import Decimal128



def create_choropleth_map( collection ):
    with open('france.geojson', 'r') as file:
        fr_map = json.load(file)       # https://france-geojson.gregoiredavid.fr/repo/departements.geojson


    pipeline = [
        {"$group": {"_id": "$Département", "Count": {"$sum": 1}}},  # Grouper par région et compter
    ]

    resultats = list(collection.aggregate(pipeline)) # Exécuter la pipeline d'agrégation

    region_counts = [{'Area': resultat['_id'], 'Count': resultat['Count']} for resultat in resultats] # Créer un dictionnaire pour les régions avec les comptes
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
        hover_data= ['Nom_region'],
        # color_continuous_scale="Viridis",
        featureidkey="properties.code",  # Ajustez ceci en fonction de la structure de votre GeoJSON
        title='Distribution des skieurs par région'
    )

    # Mise à jour de la mise en page de la figure
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":10})
    fig.update_geos(fitbounds="locations", visible=False)

    # Retourner la figure
    return fig


def average_ranking_histogram(collection):

    result = collection.aggregate([{"$addFields": {"Classement global": {"$toDecimal": "$Classement global"}}},
                                   { "$group": {"_id": "$Catégorie","average": {"$avg": "$Classement global"}}}]) 
    result_list = list(result)

    df = pd.DataFrame(result_list)
    df.rename(columns={'_id': 'Category', 'average': 'Average Ranking'}, inplace=True)
    df['Average Ranking'] = df['Average Ranking'].apply(lambda x: float(x.to_decimal()) if isinstance(x, Decimal128) else x)
    df['Category'] = df['Category'].replace({'SH': 'Seniors', 'SD': 'Seniors', 'VH': 'Masters', 'VD': 'Masters'}) # On remplace les catégories SH et SD par Seniors, et VH et VD par Masters (On ne différencie pas les sexes)

    # Regrouper par la nouvelle catégorie et recalculer la moyenne
    df = df.groupby('Category')['Average Ranking'].mean().reset_index()
    df['Average Ranking'] = df['Average Ranking'].round()
    category_order = ['U8', 'U10', 'U12', 'U14', 'U16', 'U18', 'U21', 'Seniors', 'Masters']

    df['Category'] = pd.Categorical(df['Category'], categories=category_order, ordered=True)
    df.sort_values('Category', inplace=True)
    
    # Create the bar chart
    fig = px.bar(df, x='Category', y='Average Ranking', title='Classement moyen par catégorie')

    fig.update_traces(
        texttemplate='%{y:.0f}', # On affiche les nombres entiers
        hovertemplate='<b>Catégorie:</b> %{x}<br><b>Classement moyen:</b> %{y:.0s}<extra></extra>'
    )

    fig.update_layout(
        yaxis_title='Classement moyen',
        xaxis_title='Catégorie',
        plot_bgcolor='rgba(252,248,244,1.00)',
        paper_bgcolor='cornsilk',
        font=dict(family="Montserrat", size=18, color='black')
    )
    
    # Return the figure
    return fig















# fig = average_ranking_histogram(collection)
# fig.show()




# fig = create_choropleth_map( collection )
# fig.show()