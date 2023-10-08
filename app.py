import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from components.callbacks.callback import get_callbacks
from components.content.graph_grid import render_graph_grid
from components.sidebar.sidebar import render_sidebar
from components.modals.add_graph_menu import render_graph_menu_modal
from components.topbar.topbar import render_topbar


df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

# Initialize the app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)


# App layout
app.layout = html.Div(
    style={"display": "flex", "flexDirection": "column", "height": "100vh"},
    children=[
        render_topbar(),
        html.Div(
            style={"display": "flex", "flexDirection": "row", "flex": "1"},
            children=[
                render_sidebar(),
                render_graph_grid(),
                html.Div(id="hidden-div", style={"display": "none"}),
                html.Div(id="hidden-div-dataset", style={"display": "none"}),
                html.Div(id="hidden-div-xdropdown", style={"display": "none"}),
                html.Div(id="hidden-div-ydropdown", style={"display": "none"}),
                render_graph_menu_modal(df),
            ],
        ),
    ],
)


get_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
