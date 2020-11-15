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
import pickle
import numpy as np
import zipfile
#import joblib
import dash_table
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)


server = app.server
app.config['suppress_callback_exceptions'] = True

###################################################
# Importing data
###################################################

excesos_velocidad0 = pd.read_csv("data/AlarmasExcesosVel.csv")
predicted_alarms = pd.read_csv("data/predicted_alarms.csv")
with open('data/feat_importance.json', 'r') as fp:
    feat_importance = json.load(fp)


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
                        title="Speeding Alarm Locations",
                        size_max=12,
                        zoom=4.5)



###################################################
# Generating the speeding locations map predicted
###################################################

fig_map_predictive = px.scatter_mapbox(predicted_alarms,
                        lat="latitude",
                        lon="longitude",
                        hover_name='month', hover_data=["month","EventName","idCompany", "idWorkOrder", "businessName","transporter_name"],
                        color="weekDay",
                        size="weekDay",
                        color_continuous_scale=px.colors.cyclical.Edge,
                        title="Speeding Locations Predicted",
                        size_max=12,
                        zoom=4.5)


################################################
# Generating the random forest feature importances based on the prediction model results
################################################
names = []
importance = []

for key, value in feat_importance.items():
  names.append(key)
  importance.append(value)

names = names[-10:]
importance = importance[-10:]

feature_importance = pd.DataFrame({'feature': names, 'importance': importance})

fig_feature_imp = px.bar(feature_importance, x=feature_importance.importance, y=feature_importance.feature,
                      labels={'x':'Importance', 'y': 'Feature'},color_discrete_sequence=px.colors.diverging.Portland,title="Random Forest Feature Importances (MDI)")


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
        html.Div(html.H5("Map Alarms"), className="card-header"),
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
        html.Div(html.H5("Monthly Alarms"), className="card-header"),
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
        html.Div(html.H5("Business Alarms"), className="card-header"),
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
        html.Div(html.H5("Type Operation Alarms"), className="card-header"),
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
        html.Div(html.H5("Top 30 speeding"), className="card-header"),
        html.Div(dcc.Graph(id="top30-speeding-bar"), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)


# Mapping the locations predicted
graph_map_predictive = html.Div(
    [
        html.Div(html.H5("Map Alarms"), className="card-header"),
        html.Div(dcc.Graph(id="map-predictive", figure=fig_map_predictive), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Random forest feature importances graph
graph_feature_imp = html.Div(
    [
        html.Div(html.H5("Feature Importances (Top 10)"), className="card-header"),
        html.Div(dcc.Graph(id="feature-importance", figure=fig_feature_imp), 
                 className="card-body"
        ),
    ],
    className="card",
    style=card_width
)

# Table with information of the work orders predicted with the speeding alarms model
graph_table_predictions = html.Div(
    [
        html.Div(html.H5("Predictions Table"), className="card-header"),
        html.Div(
            dash_table.DataTable(id="table",
                                 columns=[{'name':i, 'id':i} for i in predicted_alarms.loc[:,['idWorkOrder', 'latitude', 'longitude', 'businessName', 'operation_type_description', 'transporter_name']]],
                                 data=predicted_alarms.head(15).to_dict('records'),
                                 style_as_list_view=True,
                                 style_cell={'padding': '5px'},
                                 style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold',
                                    'font-family': 'Segoe UI Emoji',
                                     'font-size': '12px'
                                 },
                                 style_data={ 'font-family': 'Segoe UI Emoji',
                                                'font-size': '12px'
                                            },
                                 style_cell_conditional=[
                                {
                                    'font-family': 'Segoe UI Emoji',
                                    'if': {'column_id': ['businessName', 'operation_type_description', 'transporter_name']},
                                    'textAlign': 'left'
                                }
                                ]
                                ),className="table table-responsive"
        )
        
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
                html.Div([
                    html.P("The following map represents the result of the different speeding alarms predicted. The colors represent day of the week that the alarm could be reported based on the travel, drivers, transporters, vehicles among other information given by the company."),
                    html.P("On the other hand, the feature importance plot shows the relative importance of each feature to the prediction of the Random Forest model. A higher importance number is linked with a more relevant feature for the model. We showcase the top 10 features of the best Random Forest. As observed, date-time feature like the alarm day, alarm week and hour are the most relevant feature of the model. Followed by the alarm location as measured by the longitude and latitude. Other features like the arrival distance, specific transportation companies and operation types are less relevant.")], 
                    className="col-md-12"
                )
            ],
            style=overview_main_content
        ),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                html.Div(graph_map_predictive, className="col-md-7"),
                html.Div(graph_feature_imp, className="col-md-5")
            ],
            style=overview_main_content
        ),
        dbc.Row(
            [
                html.Div(graph_table_predictions, className="col-md-12")
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
                    html.P("We are the multidisciplinary team, who decided to tackle the business problem given by Control T. The combination of our skills made possible to understand and craft the problem, achieving a prediction model with 99% of accuracy."), 
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
                                                                html.P("Ingeniera Industrial - Universidad de los Andes | Candidate to Master in International Financial Management - Lucerne University of Applied Sciences and Arts")
                                                            ], className="card-text"),
                                                    ],className='card card-body card-block'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member2"),
                                                html.Div( 
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H5("John Ortiz"),
                                                                html.P("Ingeniero Quimico - Universidad de los Andes | MSc. Ingenieria Quimica - Universidad de los Andes | MSc. Informática - Universidad de Northeastern")
                                                            ], className="card-text"),
                                                    ],className='card card-body card-block'
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
                                                                html.P("Ingeniera de Sistemas - Universidad Distrital FJC | Esp. Construcción de Software - Universidad de los Andes | Advanced Master in Innovation and Entrepreneurship - Politecnico di Milano & ULB Solvay Brussels School")
                                                            ], className="card-text"),
                                                    ],className='card card-body card-block'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member4"),
                                                html.Div( 
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H5("Jorge mendoza"),
                                                                html.P("Estadístico - Universidad Nacional de Colombia | MSc. Estadística - Universidad Nacional de Colombia")
                                                            ], className="card-text"),
                                                    ],className='card card-body card-block'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member5"),
                                                html.Div( 
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H5("Nataly Orjuela"),
                                                                html.P("Economista - Universidad de la Salle")
                                                            ], className="card-text"),
                                                    ],className='card card-body card-block'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                html.Div(className="bd-placeholder-img card-img-top image-member6"),
                                                html.Div( 
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H5("Gabriel Triana"),
                                                                html.P("Matemático - Universidad Nacional de Colombia | MSc. Matemática Aplicada - Universidad Nacional de Colombia | Doctor en Ciencias Matemáticas - Universidad Nacional de Colombia")
                                                            ], className="card-text"),
                                                    ],className='card card-body card-block'
                                                )
                                            ],className="card mb-4 shadow-sm"
                                        )
                                    ],className="col-md-4"
                                ),
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


@app.callback(
    Output("table", "data"),
    [
        Input("map-predictive", "clickData")
    ],
)
def update_table (clickData):
    longitud = clickData['points'][0]['lon']
    latitud = clickData['points'][0]['lat']
    alarm = alarms_selected[(predicted_alarms['latitude']==latitud) & (predicted_alarms['longitude']==longitud)]
    return alarm.to_dict('records')


if __name__ == '__main__':
    app.run_server()
