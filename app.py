# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
#import seaborn as sns
import plotly.express as px
from datetime import datetime as dt
import numpy as np
#import joblib
import zipfile

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

server = app.server
app.config['suppress_callback_exceptions'] = True

###################################################
# Importing data
###################################################

#zf = zipfile.ZipFile('data/BitacoraDepurada.zip') 
#bitacora = pd.read_csv(zf.open('BitacoraDepurada.csv'))
#viajes = pd.read_csv("data/ViajesDepurados.csv")
#eventos_gps = pd.read_csv("data/eventos_gps.csv")
#conductores = pd.read_csv("data/conductores.csv")
excesos_velocidad0 = pd.read_csv("data/AlarmasExcesosVel.csv")

#vehiculos = pd.read_csv("./drive/My Drive/DS4A/Project/Final databases/vehiculos.csv")
#companias = pd.read_csv("./drive/My Drive/DS4A/Project/Final databases/compañias.csv")
#transportistas = pd.read_csv("./drive/My Drive/DS4A/Project/Final databases/transportadores.csv")

#bitacora.drop("Unnamed: 0", axis=1, inplace=True)
#viajes.drop("Unnamed: 0", axis=1, inplace=True)


###################################################
# Combining eventos GPS data base to get the event names
###################################################

#bitacora = bitacora.merge(eventos_gps, left_on="idEventGPS", right_on="IdEventsGPS")
#bitacora = bitacora.drop(["idEventGPS", "IdEventsGPS"], axis=1)
#bitacora = bitacora.rename({"name": "EventName"}, axis = 1)


#eventos_anormales = ['Fuera de ruta', 'Vehículo detenido', 'Vehículo inició marcha', 
#                    'Entrada zona alto riesgo', 'Dentro zona alto riesgo', 'No llegada a tiempo',
#                    'Botón de Paníco', 'Aproximación al destino por distancia',
#                    'Condiccion continua', 'Excesos de velocidad']

#alarmas_anomalas = bitacora.loc[bitacora["EventName"].isin(eventos_anormales)]

#alarmas_anomalas = alarmas_anomalas.merge(viajes, left_on="idWorkOrder", right_on="idWorkOrder")

#alarmas_anomalas.drop(["tipo","Country", "endLatitude", "endLongitude","inTransitTimeOn", "inTransitTimeOff", "idTrailer"], axis=1, inplace=True)

#Eliminando columnas no utilizadas en el modelo
#alarmas_presentacion = alarmas_anomalas.drop(["idMonitoringOrdersAlarm", "createdOn_y", 
#                                     "updatedOn", "updateTravelOn", "tripNumber", "city_name",
#                                     "status_name", "idStatus", "IdCondition", "transporter_name",
#                                     "idCity", "city_lon", "city_lat", "codeCity_mod",
#                                     "idCompany", "idTypeOperation", "idTypeTrip"]

#Obtener nombres de los conductores
#alarmas_presentacion = alarmas_presentacion.merge(conductores, left_on="idDriver", right_on="idDriver")
#alarmas_presentacion["Driver"] = alarmas_presentacion["name"] + " " + alarmas_presentacion["lastName"]
#alarmas_presentacion.drop(["name","lastName","idDriver"], axis=1, inplace=True)

#Obtener licencias de los vehiculos
#alarmas_presentacion = alarmas_presentacion.merge(vehiculos, left_on="idVehicle", right_on="idVehicle")
#alarmas_presentacion.drop(["idVehicle"], axis=1, inplace=True)

#Obtener nombres de los transportistas
#alarmas_presentacion = alarmas_presentacion.merge(transportistas, left_on="transporter", right_on="idCompany")
#alarmas_presentacion.drop(["transporter","idCompany","idCompanyParent"], axis=1, inplace=True)

#Renombrando variables
#alarmas_presentacion.rename({"createdOn_x":"createdOn", 
#                             "businessName_x":"CompanyName",
#                             "businessName_y":"TransporterName"}, axis=1, inplace=True)
                                             
#eventos_grupos = alarmas_anomalas.groupby("EventName")["longitude"].count().sort_values(ascending=False)

excesos_velocidad = excesos_velocidad0
#excesos_velocidad = alarmas_anomalas[alarmas_anomalas["EventName"] == 'Excesos de velocidad']
excesos_velocidad["month"].unique()

coordenadas_velocidad = excesos_velocidad.groupby(["longitude","latitude"])["idCompany"].count().sort_values(ascending=False)
coordenadas_velocidad = coordenadas_velocidad.reset_index().rename({"idCompany":"count"}, axis=1)

###################################################
# Generating the map figure
###################################################

px.set_mapbox_access_token("pk.eyJ1IjoiZHM0YXRlYW00NCIsImEiOiJja2d5ZjlkdTcwMXUwMnJybmJpNWpkZzZiIn0.NxhXaQUcuSz6VbMEFdR58A")
fig_map = px.scatter_mapbox(coordenadas_velocidad,
                        lat="latitude",
                        lon="longitude",
                        color="count",
                        size="count",
                        color_continuous_scale=px.colors.cyclical.Edge,
                        size_max=12,
                        zoom=4.5)



###################################################
# Developing the prediction
###################################################

#Xtest = pd.read_csv("data/X_test.csv")
#filename = 'data/rf_model.pkl'
#rf_v2 = joblib.load(open(filename, 'rb'))
#Xtest_copy=Xtest.copy()
#Xtest_copy=Xtest_copy.drop('Unnamed: 0',axis=1)
#Xtest_copy = Xtest_copy.astype(np.float32)
#y_pred = rf_v2.predict(Xtest_copy)
#probs = rf_v2.predict_proba(Xtest_copy)
#alarms=Xtest.loc[y_pred==1]

#indices = alarms.iloc[:,0]
#tabla_alarmas=alarmas_presentacion.loc[indices,:]

#fig_map_predictive = px.scatter_mapbox(alarms,
#                        lat="latitude",
#                       lon="longitude",
#                        hover_name='month', hover_data=["month","weekMonth", "weekDay","grouped_hours"],
#                        color="month",
#                        size="month",
#                        color_continuous_scale=px.colors.cyclical.Edge,
#                        size_max=12,
#                        zoom=4.5)


# The style arguments for the sidebar. We use position:fixed and a fixed width
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '3.5rem',
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
overview_main_content = {
    'padding-top': '1rem'
}
card_width = {
    'width': '100%'
}

# Navbar
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Team #44", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            )
        )
    ],
    color="dark",
    dark=True,
    className="site-header sticky-top py-1"
)

# Date Picker 
date_picker=dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=dt(2020, 1, 1),
                max_date_allowed=dt(2020, 10, 31),
                start_date=dt(2020,8,1).date(),
                end_date=dt(2020, 10, 11).date()
            )

# Sidebar
sidebar = html.Div(
    [
        html.H2("Control T", className="display-4"),
        html.Hr(),
        html.P(
            "Security alarms analysis for cargo transportation.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/page-1", id="link-1"),
                dbc.NavLink("Descriptive Analysis", href="/page-2", id="link-2"),
                dbc.NavLink("Predictive Analysis", href="/page-3", id="link-3"),
                dbc.NavLink("Team #44", href="/page-4", id="link-4")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


# Overview content
overview_content = html.Div(
    [
        html.H2("Context"),
        html.Hr(className="my-6"),
        dbc.Row(
            [
                html.Div([
                    html.H3("Company Information"),
                    html.P("ControlT is a company that integrates data and gives them value for timely decision making. It provides software solutions, consultancy and BPO service in the transport and logistics industry. It offers several services such as the travel’s control tower, alerts and notifications, reports, indicators and integrations."),
                    html.P("The company has around 20 people, who contribute to the fulfillment of the sustainable development goals reducing the logistic cost in Colombia. By the year 2020, ControlT has a network composed of 92 GPS companies that receive data from more than 15.000 vehicles corresponding to 89 different companies, 9 TMS/ERP platforms and 4 delivery control Apps. The customers have registered more than 300.000 trips. ControlT’s goal is to end the year 2020 with 20.000 vehicles of 100 different companies."),
                    html.Hr(className="my-8")
                    ], 
                    className="col-md-10"
                ),
                html.Div([
                    html.H3("Business Problem"),
                    html.H5("Generate smart alarms"),
                    html.P("Currently, the alarms are generated according to the preprogrammed setting of the workflow module “Conditions Matrix” which stores events that denote an alarm. For instance, a vehicle that does not move in 15 min raises a stopped vehicle alarm. To this purpose, the information received from different sources of data is processed and validated. If it meets any of the established conditions, the system generates an alert that must be attended by the traffic controllers in the module alarms."),
                    html.P("ControlT is looking for a way of generating alarms without the need of presetting manually the conditions of an alarm. Since the system raises several types of alarms under several types of conditions, the scope of this project is focused on analyzing the excess velocity alarms and panic button alarms."),
                    html.Hr(className="my-4"),
                    html.H3("Business Impact"),
                    html.H5("Benefits"),
                    html.P("-  Ensure the load so as not to have losses."),
                    html.P("-  Take alternative routes to avoid a disaster."),
                    html.P("-  Reduce costs and increase benefits."),
                    html.P("-  Identify potential risk zones."),
                    html.P("-  Quantify the risk associated with accidents and incidents in the road."),
                    html.P("-  Estimate the likelihood of a hazardous event that can impact the logistic operation.")
                    ], 
                    className="col-md-5"
                ),
                html.Div( 
                    #className="col-md-1"
                ),
                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-transport")
                                                
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-5"
                )
            ],
            style=overview_main_content
        ),
        html.Div(className="col-md-12")
    ],
    className="container-fluid"
)


# Map speeding alarms graph
graph_map = html.Div(
    [
        html.Div("Map Alarms", className="card-header"),
        html.Div(dcc.Graph(id="priority-map", figure=fig_map), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Monthly speeding alarms graph
graph_month = html.Div(
    [
        html.Div("Monthly Alarms", className="card-header"),
        html.Div(dcc.Graph(id="monthly-histogram"), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Companies whose travels reported speeding alarms
graph_business = html.Div(
    [
        html.Div("Business Alarms", className="card-header"),
        html.Div(dcc.Graph(id="business-bar"), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Type of cargo that were transported and reported speeding alarms during the trip
graph_operation = html.Div(
    [
        html.Div("Type Operation Alarms", className="card-header"),
        html.Div(dcc.Graph(id="operation-bar"), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Top 30 of locations where were reported speeding alarms 
graph_top30_excesos_velocidad = html.Div(
    [
        html.Div("Top 30 speeding", className="card-header"),
        html.Div(dcc.Graph(id="top30-speeding-bar"), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

graph_map_predictive = html.Div(
    [
        html.Div("Map Alarms", className="card-header"),
        html.Div(dcc.Graph(id="predictive-map"), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)


graph_map_predictive = html.Div(
    [
        html.Div("Map Alarms", className="card-header"),
        html.Div(dcc.Graph(id="map-predictive", figure=fig_map), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Descriptive of analytics content
descriptive_content = html.Div(
    [
        html.H2("Descriptive Analytics"),
        html.Hr(className="my-6"),
        dbc.Row(
            [
                html.Div(
                    html.P("The different graphs show an overview about the data processed. Giving information about speeding locations in Colombia, monthly speeding alarms, top 30 locations with excess of velocity and type of goods that is being transported by several companies."), 
                    className="col-md-12"
                )
            ],
            style=overview_main_content
        ),
        html.Hr(className="my-2"),
        dbc.Row(
            [
               html.Div(date_picker)
            ],
            style=overview_main_content
        ),
        dbc.Row(
            [
               html.Div(graph_map, className="col-md-12")
            ],
            style=overview_main_content
        ),
         dbc.Row(
            [
               html.Div(graph_month, className="col-md-6"),
                html.Div(graph_business, className="col-md-6")
            ],
            style=overview_main_content
        ),
        dbc.Row(
            [
               html.Div(graph_top30_excesos_velocidad, className="col-md-12")
            ],
            style=overview_main_content
        ),
         dbc.Row(
            [
               html.Div(graph_operation, className="col-md-12")
            ],
            style=overview_main_content
        )
        
    ],
    className="container-fluid"

)

# Predictive of analitycs content
predictive_content = html.Div(
    [
        html.H2("Predictive Analytics"),
        html.Hr(className="my-6"),
        dbc.Row(
            [
                html.Div(graph_map_predictive, className="col-md-12")
            ],
            style=overview_main_content
        )
    ],
    className="container-fluid"

)

# Our team content
team_content = html.Div(
    [
        html.H2("About Team #44"),
        html.Hr(className="my-6"),
        dbc.Row(
            [
                html.Div(
                    html.P("We are a multidisciplinary who decided to tackle the business problem given by Control T. The combination of our skills made possible to understand and craft the problem, achieving a prediction model with 99% of accuracy."), 
                    className="col-md-10"
                ),
                
            ],
            style=overview_main_content
        ),
        dbc.Row(
            [
                html.Div(
                    html.Div(
                        html.Div(
                            [                   
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member1"),
                                                html.Div( 
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H5("Alejandra Torres"),
                                                                html.P("Ingeniera Industrial - Universidad de los Andes")
                                                            ], className="card-text"),
                                                    ],className='card-body'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member"),
                                                html.Div( 
                                                    [
                                                        html.Div("Comming soon", className="card-text"),
                                                    ],className='card-body'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member3"),
                                                html.Div( 
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H5("Liliana Navarro"),
                                                                html.P("Ingeniera de Sistemas - Universidad Distrital FJC | Especialista en Construcción de Software - Universidad de los Andes | Advanced Master in Innovation and Entrepreneurship - Politecnico di Milano & ULB Solvay Brussels School")
                                                            ], className="card-text"),
                                                    ],className='card-body'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
								html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member"),
                                                html.Div( 
                                                    [
                                                        html.Div("Comming soon", className="card-text"),
                                                    ],className='card-body'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
								html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member"),
                                                html.Div( 
                                                    [
                                                        html.Div("Comming soon", className="card-text"),
                                                    ],className='card-body'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
								html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member"),
                                                html.Div( 
                                                    [
                                                        html.Div("Comming soon", className="card-text"),
                                                    ],className='card-body'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                )
                            ], className='row'
                        ), className='container'
                    ),className="album py-5 bg-light full-width"
                )
            ],style=overview_main_content
        )
    ]
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    sidebar, 
    content])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"link-{i}", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return overview_content
    elif pathname == "/page-2":
        return descriptive_content
    elif pathname == "/page-3":
        return predictive_content
    elif pathname == "/page-4":
        return team_content
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Updating graphs with the information gathered from range dates given by the user
@app.callback(
    Output("monthly-histogram", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    ],
)
def update_fig_month (start_date,end_date):
    excesos_velocidad2 = excesos_velocidad[(excesos_velocidad['createdOn_y'] >= start_date) 
                                           & (excesos_velocidad['createdOn_y'] <= end_date)] # We filter our dataset for the daterange
    
    fig_month = px.histogram(excesos_velocidad2,             #dataframe
                   x = "month", #x-values column
                   labels={'month': 'Month', 'count': 'Quantity'},
                             color = "month",
                             color_discrete_sequence=px.colors.cyclical.IceFire,
                             title="Number of monthly alarms",
                   nbins = 10)

    return fig_month

@app.callback(
    Output("business-bar", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    ],
)
def update_fig_business (start_date,end_date):
    excesos_velocidad2 = excesos_velocidad[(excesos_velocidad['createdOn_y'] >= start_date) 
                                           & (excesos_velocidad['createdOn_y'] <= end_date)] # We filter our dataset for the daterange
    
    fig_business = px.histogram(excesos_velocidad2,             #dataframe
                       x = "businessName", #x-values column
                       labels={'businessName':'Name of the business', 'count': 'Quantity'},color="businessName",color_discrete_sequence=px.colors.cyclical.IceFire,title="Names of the business",
                       nbins = 10        #number of bins
                       )

    return fig_business

@app.callback(
    Output("top30-speeding-bar", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    ],
)
def update_fig_top30_sepeeding (start_date,end_date):
    excesos_velocidad2 = excesos_velocidad[(excesos_velocidad['createdOn_y'] >= start_date) 
                                           & (excesos_velocidad['createdOn_y'] <= end_date)] # We filter our dataset for the daterange
    
    top_30_excesos_velocidad = excesos_velocidad2.groupby("currentLocation")["longitude"].count().sort_values(ascending=False)[:30]
    fig_topexcesos_velocidad = px.bar(excesos_velocidad2, x=top_30_excesos_velocidad.index, y=top_30_excesos_velocidad.values,
                          labels={'x':'Location', 'y': 'Number of alarms'},hover_name=top_30_excesos_velocidad.index, hover_data=[top_30_excesos_velocidad.index, top_30_excesos_velocidad.values], color=top_30_excesos_velocidad.index,color_discrete_sequence=px.colors.cyclical.IceFire,title="Top 30 locations with excess velocity")

    return fig_topexcesos_velocidad


@app.callback(
    Output("operation-bar", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    ],
)
def update_fig_operations (start_date,end_date):
    excesos_velocidad2 = excesos_velocidad[(excesos_velocidad['createdOn_y'] >= start_date) 
                                           & (excesos_velocidad['createdOn_y'] <= end_date)] # We filter our dataset for the daterange
    
    fig_operation = px.histogram(excesos_velocidad2,             #dataframe
                       x = "operation_type_description", #x-values column
                       labels={'operation_type_description':'Description operation', 'count': 'Quantity'},color="operation_type_description",color_discrete_sequence=px.colors.cyclical.IceFire,title="Type operation description",
                       nbins = 10        #number of bins
                       )

    return fig_operation



if __name__ == '__main__':
    app.run_server()
