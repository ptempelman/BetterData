from dash import Dash, html, dcc, callback, Output, Input, dash_table, dependencies, callback_context
import dash_bootstrap_components as dbc

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
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh'}, children=[
    
    # Black top bar
    html.Div(className='top-bar', children=[
        # html.H1('Top Bar', style={'color': 'white', 'width': '200px'}),

        html.Div(style={'height': '100%', 'width': '300px', 'display': 'flex'}, children=[
            html.Button(style={'marginLeft': '30px'},
                children=[
                    html.Img(src='/assets/sigma_logo.jpeg', id='overlay-image1', 
                        style={'marginTop': '0px', 'marginLeft': '0px', 'width': '30px', 'height': '30px', 'borderRadius': '50%', 'border': '2px solid #ffffff'}),
                ],
                className='square-button'
            ),
            html.Div(
                children=[
                    html.Img(src='/assets/john_face.png', id='overlay-image2', 
                        style={'marginTop': '0px', 'marginLeft': '0px', 'width': '30px', 'height': '30px', 'borderRadius': '50%', 'border': '2px solid #00b7ff'})
                ],
                className='square-button'
            ),

            html.Div(
                children=[
                    dbc.Button('+', className='btn-lg, plus'),
                ],
                className='square-button'
            ),
        ]),
        # Log In button
        html.Button('SIGN IN', className='login-button')

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
                dbc.Button('+', className='plus-sidebar')
            ])

        ]),
        
        # 2x4 grid
        html.Div(style={'flex': '1', 'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}, children=[
            html.Div(style={'flex': '1'}, children=[
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-1', n_clicks=0)
                ], className='graph-square'),
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-2', n_clicks=0)
                ], className='graph-square'),
            ]),
            
            html.Div(style={'flex': '1'}, children=[
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-3', n_clicks=0)
                ], className='graph-square'),
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-4', n_clicks=0)
                ], className='graph-square'),
            ]),
        ]),

        # The modal (popup)
        dbc.Modal([
            dbc.ModalHeader("Header"),
            dbc.ModalBody(className='modal-body', children=[
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': col, 'value': col} for col in df.columns],
                        className='dropdown',
                        value='A',
                        searchable=True,
                        placeholder='x-axis'
                    ),
                    dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': col, 'value': col} for col in df.columns],
                        className='dropdown',
                        value='B',
                        searchable=True,
                        placeholder='y-axis'
                    )
                ]),
            ]),

            dbc.ModalFooter(
                dbc.Button("Add", id="close-button", className="ml-auto")
            )
            
            # dbc.ModalFooter(
            #     dbc.Button("Close", id="close-button", className="ml-auto")
            # )
        ], id="modal", is_open=False, backdrop=True, centered=True)  # by default, set the modal to be hidden
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

@app.callback(
    Output("modal", "is_open"),
    [
        Input("open-button-1", "n_clicks"),
        Input("open-button-2", "n_clicks"),
        Input("open-button-3", "n_clicks"),
        Input("open-button-4", "n_clicks"),
        Input("close-button", "n_clicks")
    ],
    [dependencies.State("modal", "is_open")]
)
def toggle_modal(n1, n2, n3, n4, n_close, is_open):
    # Check which button was clicked by looking at dash.callback_context
    ctx = callback_context
    if not ctx.triggered:
        return is_open

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id in ["open-button-1", "open-button-2", "open-button-3", "open-button-4"]:
        return True
    elif button_id == "close-button":
        return False
    else:
        return is_open


# Run the app
if __name__ == '__main__':
    app.run(debug=True)