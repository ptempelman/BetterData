import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, Output, Input

import ssl

from components.modals.levelup_modal import render_levelup_modal

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
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"
    ],
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
                html.Div(
                    id="hidden-div-new-container-index",
                    style={"display": "none"},
                    children=[0],
                ),
                html.Div(id="hidden-div", style={"display": "none"}),
                html.Div(id="hidden-div-dataset", style={"display": "none"}),
                html.Div(
                    id="hidden-div-graph-type",
                    style={"display": "none"},
                    children="histogram",
                ),
                html.Div(id="hidden-div-xdropdown", style={"display": "none"}),
                html.Div(id="hidden-div-ydropdown", style={"display": "none"}),
                html.Div(id="hidden-div-size", style={"display": "none"}),
                html.Div(id="hidden-div-color", style={"display": "none"}),
                html.Div(id="hidden-div-hovername", style={"display": "none"}),
                html.Div(id="hidden-div-graph-prompt", style={"display": "none"}),
                html.Div(id="user-experience", style={"display": "none"}, children=0),
                html.Div(
                    id="total-modal-clicks", style={"display": "none"}, children=0
                ),
                html.Div(id="total-edit-clicks", style={"display": "none"}, children=0),
                html.Div(
                    id="menu-switch-clicks", style={"display": "none"}, children=0
                ),
                html.Div(
                    id="container-fill-type", style={"display": "none"}, children=0
                ),
                html.Div(id="confetti-trigger", style={"display": "none"}),
                html.Div(id="dummy-output", style={"display": "none"}),
                render_graph_menu_modal(df),
                render_levelup_modal(),
            ],
        ),
    ],
)


app.clientside_callback(
    """
    function(n_clicks) {
        if(n_clicks){
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
            setTimeout(function() {
                confetti.reset();
            }, 3000); // 3000 milliseconds = 3 seconds
        }
    }
    """,
    Output("dummy-output", "children"),  # Another dummy output
    [Input("confetti-trigger", "children")],
)


get_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
