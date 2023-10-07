from dash import html, dcc
import os

import data

def render_sidebar_dataset_options():
    return [
        html.Button(id=f'dynamic-sidebar-option-{filename[:-4]}', n_clicks=0, className='sidebar-option', children=[
            html.Div(filename, className='sidebar-text')
        ])
        for filename in os.listdir(os.path.dirname(data.__file__)) if filename.endswith('.csv')
    ]