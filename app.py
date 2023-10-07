from dash import Dash, html, dcc, callback, Output, Input, dash_table, dependencies, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import State
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
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-1', n_clicks=0),
                    html.Div(id='graph-container-1', className='graph-container', style={'display': 'none'})
                ], id='graph-square-1', className='graph-square'),
                
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-2', n_clicks=0),
                    html.Div(id='graph-container-2', className='graph-container', style={'display': 'none'})
                ], id='graph-square-2', className='graph-square'),
            ]),
            
            html.Div(style={'flex': '1'}, children=[
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-3', n_clicks=0),
                    html.Div(id='graph-container-3', className='graph-container', style={'display': 'none'})
                ], id='graph-square-3', className='graph-square'),
                html.Div([
                    dbc.Button([html.Div('+', className='plus-graph')], className='add-graph-area', id='open-button-4', n_clicks=0),
                    html.Div(id='graph-container-4', className='graph-container', style={'display': 'none'})
                ], id='graph-square-4', className='graph-square'),
            ]),
        ]),

        # Hidden div to save origin of graph pop up press
        html.Div(id='hidden-div', style={'display': 'none'}),

        html.Div(id='hidden-div-xdropdown', style={'display': 'none'}),
        html.Div(id='hidden-div-ydropdown', style={'display': 'none'}),

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
                dbc.Button("Add", id="add-graph-button", className="ml-auto", n_clicks=0)
            )
            
        ], id="modal", is_open=False, backdrop=True, centered=True)  # by default, set the modal to be hidden
    ])
])

@callback(
    Output('hidden-div-xdropdown', 'children'),
    Input('xaxis-column', 'value')
)
def update_xaxis(col):
    return col


@callback(
    Output('hidden-div-ydropdown', 'children'),
    Input('yaxis-column', 'value')
)
def update_xaxis(col):
    return col

@callback(
    [Output(component_id='graph-container-1', component_property='children'),
     Output(component_id='graph-container-2', component_property='children'),
     Output(component_id='graph-container-3', component_property='children'),
     Output(component_id='graph-container-4', component_property='children'),
     Output('open-button-1', 'style'),
     Output('open-button-2', 'style'),
     Output('open-button-3', 'style'),
     Output('open-button-4', 'style'),
     Output(component_id='graph-container-1', component_property='style'),
     Output(component_id='graph-container-2', component_property='style'),
     Output(component_id='graph-container-3', component_property='style'),
     Output(component_id='graph-container-4', component_property='style'),
     Output("modal", "is_open", allow_duplicate=True)],
    [Input(component_id='add-graph-button', component_property='n_clicks')],
    [State('hidden-div', 'children'),
     State('hidden-div-xdropdown', 'children'),
     State('hidden-div-ydropdown', 'children'),
     State('open-button-1', 'style'),
     State('open-button-2', 'style'),
     State('open-button-3', 'style'),
     State('open-button-4', 'style'),
     State('graph-container-1', 'children'),
     State('graph-container-2', 'children'),
     State('graph-container-3', 'children'),
     State('graph-container-4', 'children'),
     State('graph-container-1', 'style'),
     State('graph-container-2', 'style'),
     State('graph-container-3', 'style'),
     State('graph-container-4', 'style'),
     ],
    prevent_initial_call=True
    )
def add_graph(n, btn_id, xcol, ycol, vis1, vis2, vis3, vis4, gc1, gc2, gc3, gc4, gv1, gv2, gv3, gv4):

    graph = dcc.Graph(figure=px.histogram(df, x=xcol, y=ycol, histfunc='avg'), className='main-graph', \
                         config = {'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'pan', 'select2d', 'lasso2d', 'autoscale']})
    
    inv = {'display': 'none'}
    vis = {'display': 'unset'}
    if btn_id == 'open-button-1':
        return [graph], gc2, gc3, gc4, \
            inv, vis2, vis3, vis4, \
            vis, gv2, gv3, gv4, False
    if btn_id == 'open-button-2':
        return gc1, [graph], gc3, gc4, \
            vis1, inv, vis3, vis4, \
            gv1, vis, gv3, gv4, False
    if btn_id == 'open-button-3':
        return gc1, gc2, [graph], gc4, \
            vis1, vis2, inv, vis4, \
            gv1, gv2, vis, gv4, False
    else:
        return gc1, gc2, gc3, [graph], \
            vis1, vis2, vis3, inv, \
            gv1, gv2, gv3, vis, False

@app.callback(
    [Output("modal", "is_open", allow_duplicate=True),
     Output('hidden-div', 'children')],
    [
        Input("open-button-1", "n_clicks"),
        Input("open-button-2", "n_clicks"),
        Input("open-button-3", "n_clicks"),
        Input("open-button-4", "n_clicks"),
    ],
    [dependencies.State("modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_modal(b1, b2, b3, b4, is_open):
    ctx = callback_context
    if not ctx.triggered:
        return False, 'nothing'
    else:
        return True, ctx.triggered[0]['prop_id'].split('.')[0]


# Run the app
if __name__ == '__main__':
    app.run(debug=True)