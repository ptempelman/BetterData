from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import data


def render_graph_menu_modal(df):
    return dbc.Modal(
        [
            dbc.ModalHeader(
                children=[
                    html.Button(
                        id={"type": "add-menu-type", "index": 0},
                        className="view-menu-button",
                        n_clicks=0,
                        children=[
                            html.Img(
                                src="assets/bar_chart_FILL0_wght400_GRAD0_opsz24.svg",
                            )
                        ],
                    ),
                    html.Button(
                        id={"type": "add-menu-type", "index": 1},
                        className="view-menu-button",
                        n_clicks=0,
                        children=[
                            html.Img(
                                src="assets/table_FILL0_wght400_GRAD0_opsz24.svg",
                            )
                        ],
                    ),
                ]
            ),
            dbc.ModalBody(
                className="modal-body",
                children=[
                    html.Div(
                        id={"type": "menu-type", "index": 0},
                        children=[
                            html.Div(
                                id="metadata-graph",
                                children=[
                                    dcc.Dropdown(
                                        id="dataset-dropdown",
                                        options=[
                                            {"label": filename, "value": filename}
                                            for filename in os.listdir(
                                                os.path.dirname(data.__file__)
                                            )
                                            if filename.endswith(".csv")
                                        ],
                                        className="dropdown",
                                        value="",
                                        searchable=True,
                                        placeholder="dataset",
                                    ),
                                    dcc.Dropdown(
                                        id="graph-type-dropdown",
                                        options=[
                                            {
                                                "label": "histogram",
                                                "value": "histogram",
                                            },
                                            {
                                                "label": "scatterplot",
                                                "value": "scatterplot",
                                            },
                                        ],
                                        className="dropdown",
                                        value="",
                                        searchable=True,
                                        placeholder="graph type",
                                    ),
                                ],
                            ),
                            dcc.Dropdown(
                                id="xaxis-column",
                                options=[
                                    {"label": col, "value": col} for col in df.columns
                                ],
                                className="dropdown",
                                value="A",
                                searchable=True,
                                placeholder="x-axis",
                            ),
                            dcc.Dropdown(
                                id="yaxis-column",
                                options=[
                                    {"label": col, "value": col} for col in df.columns
                                ],
                                className="dropdown",
                                value="B",
                                searchable=True,
                                placeholder="y-axis",
                            ),
                        ],
                    ),
                    html.Div(
                        id={"type": "menu-type", "index": 1},
                        style={"display": "none"},
                        children=[
                            dcc.Dropdown(
                                id="dataset-dropdown-table",
                                options=[
                                    {"label": filename, "value": filename}
                                    for filename in os.listdir(
                                        os.path.dirname(data.__file__)
                                    )
                                    if filename.endswith(".csv")
                                ],
                                className="dropdown",
                                value="",
                                searchable=True,
                                placeholder="dataset",
                            )
                        ],
                    ),
                ],
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Add",
                    id={"type": "add-graph-button", "index": 0},
                    className="ml-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="modal",
        is_open=False,
        backdrop=True,
        centered=True,
    )
