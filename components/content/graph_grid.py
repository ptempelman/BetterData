from dash import html
import dash_bootstrap_components as dbc
import dash_draggable
import pandas as pd
from dash import dcc

from components.content.dashboard_item import render_dashboard_item


def render_graph_grid():
    return html.Div(
        id="content-container",
        children=[
            # html.Button(
            #     id="view-menu",
            #     n_clicks=0,
            #     children=[
            #         html.Img(
            #             id="view-menu-img",
            #             src="assets/bar_chart_FILL0_wght400_GRAD0_opsz24.svg",
            #         )
            #     ],
            # ),
            # Table view: filled by callback
            html.Div(id="table-view-container", style={"display": "none"}),
            html.Div(
                id="graph-view-container",
                className="grid-container",
                children=[
                    dash_draggable.ResponsiveGridLayout(
                        height=100,
                        save=True,
                        id="draggable",
                        resizeHandles=[
                            "se",
                            "s",
                            "e",
                        ],  # , 'n', 'w', 'e', 's'],
                        children=[render_dashboard_item(0)],
                    )
                ],
            ),
        ],
    )
