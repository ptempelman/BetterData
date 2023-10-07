from dash import html
import os

import data

def render_sidebar_dataset_options():
    return [
        html.Div(className='sidebar-option', children=[
            html.Div(filename, className='sidebar-text')
        ])
        for filename in os.listdir(os.path.dirname(data.__file__)) if filename.endswith('.csv')
    ]