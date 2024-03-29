import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from graphs import *
from dash.dependencies import State

#connection a la db pour recuperer les données
client = MongoClient('mongodb', 27017)
db = client['esf']
collection = db['ecoles']
collection_skieurs = db['skieurs']

#application dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

df_moni = dataFrame_moniteurs() #création de dataframe
df_info = dataFrame_infoStation() #création de dataframe

# Créer l'app Dash
app.layout = html.Div([
    # Sidebar pour afficher les 2 différentes données
    html.Div([
        html.H2('Sidebar'),
        dcc.Link('Ecoles', href='/ecoles'),
        html.Br(),  # Add a line break
        dcc.Link('Classement', href='/classement')
    ], style={'width': '20%', 'position': 'fixed', 'height': '100%', 'backgroundColor': '#f8f9fa'}),

    html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', style={'padding': '20px'})
    ], style={'marginLeft': '20%'}),

])


# Callback pour afficher/cacher la Checklist en fonction de l'onglet sélectionné
@app.callback(
    Output('checkbox-moniteurs-anglais', 'style'),
    [Input('ecoles-tabs', 'value')]
)
def update_checkbox_visibility(selected_tab):
    if selected_tab == 'tab-1':
        return {'position': 'fixed', 'bottom': '250px', 'right': '30px', 'display': 'block'}
    else:
        return {'display': 'none'}

# callback pour afficher les graphiques selon les tabs pour le sidebar ecole
@app.callback(
    Output('ecoles-tabs-content', 'children'),
    [Input('ecoles-tabs', 'value'),
     Input('checkbox-moniteurs-anglais', 'value')]
)
def update_ecoles_tab(selected_tab, checkbox_value):
    if selected_tab == 'tab-1':
        if checkbox_value:
            return html.Div([
                dcc.Graph(id='graph1', figure=create_histo_moni_anglais(df_moni)),
                html.Div(
                    id='description1',
                    children="On compte le nombre de moniteurs parlant anglais par station, et on regarde ici le nombre de stations contenant un certain nombre de moniteurs.",
                    # Description du graphique
                    style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}
                    # Visuel de la description
                )
            ])
        else:
            return html.Div([
                dcc.Graph(id='graph1', figure=create_histo_moni(df_moni)),
                html.Div(
                    id='description1',
                    children="On compte le nombre de moniteurs par station, et on regarde ici le nombre de stations contenant un certain nombre de moniteurs.",
                    # Description du graphique
                    style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}
                    # Visuel de la description
                )
            ])
    elif selected_tab == 'tab-2':
        return html.Div([
            dcc.Graph(id='graph2', figure=create_histo_km_piste(df_info)),
            html.Div(
                id='description2',
                children="Ce graphique montre le nombre de kilomètres de piste cumulés par station.",
                # Description du graphique
                style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}  # Visuel de la description
            )
        ])
    elif selected_tab == 'tab-3':
        return html.Div([
            dcc.Graph(id='graph3', figure=create_histo_remonte(df_info)),
            html.Div(
                id='description3',
                children="Ce graphique montre le nombre de remontées mécaniques par station.",
                # Description du graphique
                style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}  # Visuel de la description
            )
        ])
    elif selected_tab == 'tab-4':
        return html.Div([
            dcc.Graph(id='graph4', figure=create_histo_snowparks(df_info)),
            html.Div(
                id='description4',
                children="Ce graphique montre le sowparks par station.",  # Description du graphique
                style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}  # Visuel de la description
            )
        ])
    elif selected_tab == 'tab-5':
        return html.Div([
            dcc.Graph(id='graph5', figure=create_choropleth_map(collection_skieurs)),
            html.Div(
                id='description5',
                children="Cette carte permet de d'observer le nombre de skieurs par région en France. Au survol, vous pouvez obtenir le nom de chaque région et son nombre précis de skieurs enregistrés.",
                # Description du graphique
                style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}  # Visuel de la description
            )
        ])
    elif selected_tab == 'tab-6':
        return html.Div([
            dcc.Graph(id='graph6', figure=average_ranking_histogram(collection_skieurs)),
            html.Div(
                id='description6',
                children="Cet histogramme montre le rang moyen pour chaque catégorie d'age.",
                # Description du graphique
                style={'text-align': 'center', 'font-size': '15px', 'margin-top': '50px'}  # Visuel de la description
            )
        ])


    # callback pour afficher les graphiques selon les tabs pour le sidebar classement
@app.callback(
    Output('classement-tabs-content', 'children'),
    [Input('classements-tabs', 'value')]
)
def update_classements_tab(selected_tab):
    if selected_tab == 'tab-5':
        return dcc.Graph(figure=create_choropleth_map(collection_skieurs))
    elif selected_tab == 'tab-6':
        return dcc.Graph(figure=average_ranking_histogram(collection_skieurs))


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('url', 'href')]
)
def display_page(pathname, href):
    # Redirection à /ecoles pour le début
    if pathname == '/':
        return dcc.Location(href='/ecoles', id='redirect-to-ecoles')

    if pathname == '/ecoles':
        return html.Div([
            # Tabs pour la page Ecoles
            dcc.Tabs(
                id='ecoles-tabs',
                value='tab-1',
                children=[
                    dcc.Tab(label='Moniteurs', value='tab-1'),
                    dcc.Tab(label='Kilomètres de Piste', value='tab-2'),
                    dcc.Tab(label='Remontées Mécaniques', value='tab-3'),
                    dcc.Tab(label='Snowparks', value='tab-4'),
                ],
                style={'marginTop': '20px'}
            ),
            #checklist pour moniteur parlant anglais ou non
            html.Div([
                dcc.Checklist(
                    id='checkbox-moniteurs-anglais',
                    options=[
                        {'label': 'Moniteurs parlant anglais', 'value': 'anglais'}
                    ],
                    value=[],
                    labelStyle={'display': 'block'}
                )
            ], style={'position': 'fixed', 'bottom': '350px', 'right': '20px'}),

            html.Div(id='ecoles-tabs-content')
        ])


    elif pathname == '/classement':
        return html.Div([
            # Tabs pour la page classement
            dcc.Tabs(
                id='classements-tabs',
                value='tab-5',
                children=[
                    dcc.Tab(label='Carte des skieurs', value='tab-5'),
                    dcc.Tab(label='Classement par catégorie', value='tab-6'),
                ],
                style={'marginTop': '20px'}
            ),
            html.Div(id='classement-tabs-content')

        ])
    else:
        # si l'url n'est pas connue
        return "404 Page Not Found"

#pour run en localhost
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)






