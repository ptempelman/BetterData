from dash import html
import dash_bootstrap_components as dbc
import dash_draggable
import pandas as pd
from dash import dcc


def render_graph_grid():
    return html.Div(
        id="content-container",
        children=[
            html.Button(
                id="view-menu",
                n_clicks=0,
                children=[
                    html.Img(
                        id="view-menu-img",
                        src="assets/bar_chart_FILL0_wght400_GRAD0_opsz24.svg",
                    )
                ],
            ),
            # Table view: filled by callback
            html.Div(id="table-view-container", style={"display": "none"}),
            html.Div(
                id="graph-view-container",
                className="grid-container",
                children=[
                    dash_draggable.ResponsiveGridLayout(
                        save=True,
                        id="draggable",
                        resizeHandles=[
                            "se",
                            "sw",
                            "ne",
                            "nw",
                        ],  # , 'n', 'w', 'e', 's'],
                        children=[
                            dash_draggable.DashboardItem(
                                i='draggable-0',
                                h=9,
                                w=6,
                                minH=2,
                                minW=2,
                                x=0,
                                y=0,
                                children=[
                                    html.Div(
                                        [
                                            dbc.Button(
                                                [html.Div("+", className="plus-graph")],
                                                className="add-graph-area",
                                                id={"type": "open-button", "index": 0},
                                                n_clicks=0,
                                            ),
                                            html.Div(
                                                id={
                                                    "type": "filled-container",
                                                    "index": 0,
                                                },
                                                className="filled-container",
                                                style={"display": "none"},
                                                children=[
                                                    html.Div(
                                                        id={
                                                            "type": "graph-menu-options",
                                                            "index": 0,
                                                        },
                                                        className="graph-menu-options",
                                                        children=[
                                                            html.Button(
                                                                id={
                                                                    "type": "graph-menu-edit",
                                                                    "index": 0,
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
                                                                    "index": 0,
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
                                                            "index": 0,
                                                        },
                                                        className="graph-container",
                                                    ),
                                                ],
                                            ),
                                        ],
                                        id={"type": "graph-square", "index": 0},
                                        className="graph-square",
                                    )
                                ]
                            ),
                        ],
                    )
                ],
            ),
            # html.Div(
            #     id="graph-view-container",
            #     className="grid-container",
            #     children=[
            #         html.Div(
            #             className="grid-item",
            #             children=[
            #                 html.Div(
            #                     [
            #                         dbc.Button(
            #                             [html.Div("+", className="plus-graph")],
            #                             className="add-graph-area",
            #                             id=f"open-button-{i}",
            #                             n_clicks=0,
            #                         ),
            #                         html.Div(
            #                             id=f"filled-container-{i}",
            #                             className="filled-container",
            #                             style={"display": "none"},
            #                             children=[
            #                                 html.Div(
            #                                     id=f"graph-menu-options-{i}",
            #                                     className="graph-menu-options",
            #                                     children=[
            #                                         html.Button(
            #                                             id=f"graph-menu-edit-{i}",
            #                                             className="graph-menu-button",
            #                                             children=html.Img(
            #                                                 className="graph-menu-button-img",
            #                                                 src="assets/edit_FILL0_wght400_GRAD0_opsz24.svg",
            #                                             ),
            #                                         ),
            #                                         html.Button(
            #                                             id=f"graph-menu-delete-{i}",
            #                                             className="graph-menu-button",
            #                                             children=html.Img(
            #                                                 src="assets/delete_FILL0_wght400_GRAD0_opsz24.svg"
            #                                             ),
            #                                         ),
            #                                     ],
            #                                 ),
            #                                 html.Div(
            #                                     id=f"graph-container-{i}",
            #                                     className="graph-container",
            #                                 ),
            #                             ],
            #                         ),
            #                     ],
            #                     id=f"graph-square-{i}",
            #                     className="graph-square",
            #                 )
            #             ],
            #         )
            #         for i in range(1, 5)
            #     ],
            # ),
        ],
    )
