from dash import Dash, html, dcc, callback, Output, Input, dash_table

import plotly.express as px
import pandas as pd
import data
import os.path as osp
import os

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# df = pd.read_csv(osp.join(osp.dirname(data.__file__), 'house_prices.csv'))

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh'}, children=[
    
    # Black top bar
    html.Div(className='top-bar', children=[
        # html.H1('Top Bar', style={'color': 'white', 'width': '200px'}),

        html.Div(style={'height': '100%', 'width': '300px', 'display': 'flex'}, children=[
            html.Button(style={'margin-left': '30px'},
                children=[
                    html.Img(src='/assets/sigma_logo.jpeg', id='overlay-image1', 
                        style={'margin-top': '0px', 'margin-left': '0px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #ffffff'}),
                ],
                className='square-button'
            ),
            html.Button(
                children=[
                    html.Img(src='/assets/john_face.png', id='overlay-image2', 
                        style={'margin-top': '0px', 'margin-left': '0px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #00b7ff'})
                ],
                className='square-button'
            ),

            html.Button(
                children=[
                    html.Div(className='plus'),
                    # html.Img(src='/assets/pixil-frame-0 (1).png', id='overlay-image2', 
                    #     style={'margin-top': '0px', 'margin-left': '0px', 'width': '20px', 'height': '20px', 'fill': 'white'})
                ],
                className='square-button'
            ),
        ]),
        # Log In button
        html.Button('Sign In', className='login-button')

    ]),
    
    # Main content area with sidebar and grid
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'flex': '1'}, children=[
        
        # Black left sidebar
        html.Div(className='sidebar', children=[
            html.Div(className='sidebar-title', children=[
                html.Div('DATASETS', className='sidebar-title-inner')
            ]),

            # Sidebar dataset options
            html.Div(children=[html.Div(className='sidebar-option', children=[
                html.Div(filename, className='sidebar-text')
            ])
                               for filename in os.listdir('data/') if filename.endswith('.csv')]),
            html.Div(className='sidebar-add-button', children=[
                html.Div(className='plus-sidebar')
            ])

        ]),
        
        # 2x4 grid
        html.Div(style={'flex': '1', 'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}, children=[
            html.Div(style={'flex': '1'}, children=[
                html.Div([
                    html.Div([html.Div(className='plus-graph')], className='add-graph-button')
                ], className='graph-square'),
                html.Div([
                    html.Div([html.Div(className='plus-graph')], className='add-graph-button')
                ], className='graph-square'),
            ]),
            
            html.Div(style={'flex': '1'}, children=[
                html.Div([
                    html.Div([html.Div(className='plus-graph')], className='add-graph-button')
                ], className='graph-square'),
                html.Div([
                    html.Div([html.Div(className='plus-graph')], className='add-graph-button')
                ], className='graph-square'),
            ]),
        ])
    ])
])

# html.Div(style={'height': '100vh', 'margin': '0', 'width': '100vw'}, children=[

#     # New vertical column div on the left
#     # html.Div(style={'backgroundColor': 'black', 'width': '100px', 'height': '100%'}),

#     # The rest of your layout
#     html.Div(children=[
        
#         html.Div(children=[
#             html.Img(src='/assets/sigma_logo.jpeg', id='overlay-image1', 
#                      style={'margin-top': '3px', 'margin-left': '10px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #ffffff'}),
            
#             html.Img(src='/assets/john_face.png', id='overlay-image2', 
#                      style={'margin-top': '3px', 'margin-left': '10px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #00b7ff'})
#         ],
#         style={'textAlign': 'left', 'color': 'blue', 'fontSize': 30, 'background-color': 'black', 
#                'padding': 0, 'width': '100%', 'height': '40px'}),

#         html.Div(className='row', children=[
#             dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
#                            value='lifeExp',
#                            inline=True,
#                            id='my-radio-buttons-final')
#         ]),

#         html.Div(className='row', children=[
#             html.Div(className='six columns', children=[
#                 dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
#             ]),
#             html.Div(className='six columns', children=[
#                 dcc.Graph(figure={}, id='histo-chart-final')
#             ])
#         ])

#     ])
# ])

# Add controls to build the interaction
# @callback(
#     Output(component_id='histo-chart-final', component_property='figure'),
#     Input(component_id='my-radio-buttons-final', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)