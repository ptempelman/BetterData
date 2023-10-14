from dash import html
import dash_bootstrap_components as dbc
import dash_draggable
import pandas as pd
from dash import dcc


def render_dashboard_item(index):
    return dash_draggable.DashboardItem(
        i=f"draggable-{index}",
        h=2,
        w=5,
        minH=2,
        minW=2,
        x=0,
        y=0,
        children=[
            html.Div(
                id={"type": "graph-square", "index": index},
                className="graph-square",
                children=[
                    dbc.Button(
                        [html.Div("+", className="plus-graph")],
                        className="add-graph-area",
                        id={"type": "open-button", "index": index},
                        n_clicks=0,
                    ),
                    html.Div(
                        id={
                            "type": "filled-container",
                            "index": index,
                        },
                        className="filled-container",
                        style={"display": "none"},
                        children=[
                            html.Div(
                                id={
                                    "type": "graph-menu-options",
                                    "index": index,
                                },
                                className="graph-menu-options",
                                children=[
                                    html.Button(
                                        id={
                                            "type": "graph-menu-edit",
                                            "index": index,
                                        },
                                        className="graph-menu-button",
                                        children=html.Img(
                                            className="graph-menu-button-img",
                                            src="assets/edit_FILL0_wght400_GRAD0_opsz24.svg",
                                        ),
                                    ),
                                    html.Button(
                                        id={
                                            "type": "graph-menu-delete",
                                            "index": index,
                                        },
                                        className="graph-menu-button",
                                        children=html.Img(
                                            src="assets/delete_FILL0_wght400_GRAD0_opsz24.svg"
                                        ),
                                    ),
                                ],
                            ),
                            html.Div(
                                id={
                                    "type": "graph-container",
                                    "index": index,
                                },
                                className="graph-container",
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
