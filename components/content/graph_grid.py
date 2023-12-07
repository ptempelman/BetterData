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
