from dash import html
import dash_bootstrap_components as dbc

def render_graph_grid():
    return html.Div(style={'flex': '1', 'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'position': 'relative'}, children=[
            
            
            html.Button(id='view-menu', n_clicks=0, children=[
                html.Img(id='view-menu-img', src='assets/bar_chart_FILL0_wght400_GRAD0_opsz24.svg')
            ]),


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
        ])