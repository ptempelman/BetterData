from dash import html, dcc
import dash_bootstrap_components as dbc


def render_graph_menu_modal(df):
    return dbc.Modal(
        [
            dbc.ModalHeader("Header"),
            dbc.ModalBody(
                className="modal-body",
                children=[
                    html.Div(
                        [
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
                        ]
                    ),
                ],
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Add", id="add-graph-button", className="ml-auto", n_clicks=0
                )
            ),
        ],
        id="modal",
        is_open=False,
        backdrop=True,
        centered=True,
    )
