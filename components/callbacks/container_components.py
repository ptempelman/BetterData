from dash import (
    dcc,
    callback,
    Output,
    Input,
    State,
    callback_context,
    dependencies,
    MATCH,
    ALL,
    no_update,
)
import pandas as pd
import plotly.express as px
from components.content.dashboard_item import render_dashboard_item
import data
import os
import os.path as osp
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import html
import dash_bootstrap_components as dbc
import dash_draggable


def get_graph(ctx, ds, graph_type, xcol, ycol):
    print(f"graph added to {ctx.triggered[0]['prop_id'].split('.')[0]}")

    if graph_type == "histogram":
        graph = dcc.Graph(
            figure=px.histogram(
                pd.read_csv(osp.join(osp.dirname(data.__file__), ds)),
                x=xcol,
                y=ycol,
                histfunc="avg",
                template="plotly_dark",
            ),
            className="main-graph",
            config={
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom",
                    "pan",
                    "select2d",
                    "lasso2d",
                    "autoscale",
                ],
            },
        )
    else:  #  elif graph_type == "scatterplot":
        graph = dcc.Graph(
            figure=px.scatter(
                pd.read_csv(osp.join(osp.dirname(data.__file__), ds)),
                x=xcol,
                y=ycol,
                template="plotly_dark",
            ),
            className="main-graph",
            config={
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom",
                    "pan",
                    "select2d",
                    "lasso2d",
                    "autoscale",
                ],
            },
        )

    return graph


def get_table(ds):
    df = pd.read_csv(osp.join(osp.dirname(data.__file__), ds))

    table = dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_header={
            "color": "white",
            "background-color": "#7d7d7d",
            "border": "1px solid black",
        },
        style_cell={"border": "1px solid grey"},
    )

    return table