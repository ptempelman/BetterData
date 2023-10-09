from dash import html
import dash_bootstrap_components as dbc
from components.sidebar.options import render_sidebar_dataset_options


def render_sidebar():
    return html.Div(
        className="sidebar",
        children=[
            html.Div(
                className="sidebar-title",
                children=[html.Div("DATASETS", className="sidebar-title-inner")],
            ),
            *render_sidebar_dataset_options(),
            html.Div(
                className="sidebar-add-button",
                children=[dbc.Button("+", className="plus-sidebar")],
            ),
        ],
    )
