from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import data
import os.path as osp

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# df = pd.read_csv(osp.join(osp.dirname(data.__file__), 'house_prices.csv'))

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div(style={'height': '100vh', 'margin': '0', 'width': '100vw'}, children=[

    # New vertical column div on the left
    # html.Div(style={'backgroundColor': 'black', 'width': '100px', 'height': '100%'}),

    # The rest of your layout
    html.Div(children=[
        
        html.Div(children=[
            html.Img(src='/assets/sigma_logo.jpeg', id='overlay-image1', 
                     style={'margin-top': '3px', 'margin-left': '10px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #ffffff'}),
            
            html.Img(src='/assets/john_face.png', id='overlay-image2', 
                     style={'margin-top': '3px', 'margin-left': '10px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #00b7ff'})
        ],
        style={'textAlign': 'left', 'color': 'blue', 'fontSize': 30, 'background-color': 'black', 
               'padding': 0, 'width': '100%', 'height': '40px'}),

        html.Div(className='row', children=[
            dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                           value='lifeExp',
                           inline=True,
                           id='my-radio-buttons-final')
        ]),

        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='histo-chart-final')
            ])
        ])

    ])
])

# Add controls to build the interaction
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)