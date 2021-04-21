# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# https://www.rapidtables.com/web/color/RGB_Color.html
# colors: https://plotly.com/python/discrete-color/
# histogram barmode: https://towardsdatascience.com/histograms-with-plotly-express-complete-guide-d483656c5ad7
# interactive graphs: https://dash.plotly.com/interactive-graphing

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import seaborn as sns

import style
import data

app = dash.Dash(__name__, external_stylesheets= style.external_stylesheets)

############# DATA #############

df, df_test = data.eda()
categories_cat = np.array(['Sex', 'Embarked', 'Pclass', 'Cabin_1', 'Title'])
categories_num = np.array(['Age', 'Fare', 'Parch', 'SibSp'])
colors = np.array([style.colors['red'], style.colors['green'], style.colors['yellow']])


############# PLOTS #############
@app.callback(
    Output("bar_chart_1", "figure"), 
    [Input("dropdown_cat", "value")])
def update_bar_chart_1(category):
    fig = px.histogram(x=df[category],
        title= ('Histogram for '+ category),
        labels = dict(x= category),
        width = 500)
    return fig

@app.callback(
    Output("bar_chart_2", "figure"), 
    [Input("dropdown_cat", "value")])
def update_bar_chart_2(category):
    fig = px.histogram(x=df[category], color=df['Survived'], 
        barmode= 'group', color_discrete_sequence= colors, 
        title= ('Survived given '+ category),
        labels = dict(x= category),
        width = 500)
    return fig

@app.callback(
    Output("bar_chart_3", "figure"), 
    [Input("dropdown_num", "value")])
def update_bar_chart_1(category):
    fig = px.histogram(x=df[category],
        title= ('Histogram for '+ category),
        labels = dict(x= category),
        width = 500)
    return fig


@app.callback(
    Output("distplot", "figure"), 
    [Input("dropdown_num", "value")])
def update_distPlot(category):
    surv = df[category].loc[df['Survived'] == 1]
    notSurv = df[category].loc[df['Survived'] == 0]
    surv_per_age = [notSurv, surv]
    fig = px.histogram(surv_per_age,
        barmode= 'group', color_discrete_sequence= colors, 
        color=['Not Survived', 'Survived'],marginal="box",
        title= ('Survived given '+ category),
        labels = dict(x= category))
    return fig


############# METHODS #############

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def pivot():
    pivot = pd.pivot_table(df, 
                index = 'Survived', 
                values = ['Age', 'SibSp', 'Parch', 'Fare'])
    return pivot

############# LAYOUT #############

app.layout = html.Div(
    style={'backgroundColor': style.colors['background']}, 
    children=[
        html.H2(
            children='Titanic kaggle challenge',
            style={
                'textAlign': 'left',
                'color': style.colors['text']
        }),
   
    dcc.Dropdown(
       id="dropdown_cat",
        options=[{"label": x, "value": x} for x in categories_cat],
        value= categories_cat[0],
        clearable=False,
        style={'width': '50%', 'display': 'inline-block'}),
        
    dcc.Graph(id="bar_chart_1"),
    dcc.Graph(id="bar_chart_2"),

    dcc.Dropdown(
       id="dropdown_num",
        options=[{"label": x, "value": x} for x in categories_num],
        value= categories_num[0],
        clearable=False,
        style={'width': '50%', 'display': 'inline-block'}),

    dcc.Graph(id="bar_chart_3"),
    dcc.Graph(id="distplot")
    
])

if __name__ == '__main__':
    app.run_server(debug=True)