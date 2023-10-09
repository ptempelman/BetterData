from dash import dcc, callback, Output, Input, State, callback_context, dependencies
import pandas as pd
import plotly.express as px
import data
import os
import os.path as osp
from dash import dash_table


def get_callbacks(app):
    filenames = [
        filename[:-4]
        for filename in os.listdir(os.path.dirname(data.__file__))
        if filename.endswith(".csv")
    ]

    @app.callback(
        [
            Output(f"dynamic-sidebar-option-{filename}", "className")
            for filename in filenames
        ]
        + [
            Output("hidden-div-dataset", "children"),
            Output("xaxis-column", "options"),
            Output("yaxis-column", "options"),
            Output("table-view-container", "children"),
        ],
        [
            Input(f"dynamic-sidebar-option-{filename}", "n_clicks")
            for filename in filenames
        ],
        prevent_initial_call=True,
    )
    def update_button_color(*btn_clicks):
        ctx = callback_context
        clicked_btn_id = ctx.triggered[0]["prop_id"].split(".")[0]

        default_style = "sidebar-option"
        active_style = "sidebar-option-selected"
        styles = [default_style for _ in range(len(filenames))]

        if clicked_btn_id.rsplit("-", 1)[-1] in filenames:
            clicked_btn_index = filenames.index(clicked_btn_id.rsplit("-", 1)[-1])
            styles[clicked_btn_index] = active_style

        filename = clicked_btn_id.replace("dynamic-sidebar-option-", "") + ".csv"
        fileloc = osp.join(osp.dirname(data.__file__), filename)

        df = pd.read_csv(fileloc)
        options = [{"label": col, "value": col} for col in df.columns]

        table_view = dash_table.DataTable(
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

        return styles + [filename, options, options, [table_view]]

    @callback(
        Output("hidden-div-xdropdown", "children"), Input("xaxis-column", "value")
    )
    def update_xaxis(col):
        return col

    @callback(
        Output("hidden-div-ydropdown", "children"), Input("yaxis-column", "value")
    )
    def update_yaxis(col):
        return col

    @callback(
        Output("hidden-div-graph-type", "children"),
        Input("graph-type-dropdown", "value"),
    )
    def update_graph_type(graph_type):
        return graph_type

    @callback(
        [
            Output(f"graph-container-{i + 1}", "children", allow_duplicate=True)
            for i in range(4)
        ]
        + [
            Output(f"open-button-{i + 1}", "style", allow_duplicate=True)
            for i in range(4)
        ]
        + [
            Output(f"filled-container-{i + 1}", "style", allow_duplicate=True)
            for i in range(4)
        ]
        + [Output("modal", "is_open", allow_duplicate=True)],
        [Input("add-graph-button", "n_clicks")],
        [
            State("hidden-div", "children"),
            State("hidden-div-xdropdown", "children"),
            State("hidden-div-ydropdown", "children"),
            State("hidden-div-graph-type", "children"),
        ]
        + [State(f"open-button-{i + 1}", "style") for i in range(4)]
        + [State(f"graph-container-{i + 1}", "children") for i in range(4)]
        + [State(f"filled-container-{i + 1}", "style") for i in range(4)]
        + [State("hidden-div-dataset", "children")],
        prevent_initial_call=True,
    )
    def add_graph(
        n,
        btn_id,
        xcol,
        ycol,
        graph_type,
        vis1,
        vis2,
        vis3,
        vis4,
        gc1,
        gc2,
        gc3,
        gc4,
        gv1,
        gv2,
        gv3,
        gv4,
        ds,
    ):
        print(graph_type)
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
        elif graph_type == "scatterplot":
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

        inv = {"display": "none"}
        vis = {"display": "unset"}

        idx = int(btn_id[-1]) - 1

        graphs = [gc1, gc2, gc3, gc4]
        button_vis = [vis1, vis2, vis3, vis4]
        graph_vis = [gv1, gv2, gv3, gv4]

        graphs[idx] = [graph]
        button_vis[idx] = inv
        graph_vis[idx] = vis

        return graphs + button_vis + graph_vis + [False]

    @app.callback(
        [
            Output("modal", "is_open", allow_duplicate=True),
            Output("hidden-div", "children", allow_duplicate=True),
        ],
        [
            Input("open-button-1", "n_clicks"),
            Input("open-button-2", "n_clicks"),
            Input("open-button-3", "n_clicks"),
            Input("open-button-4", "n_clicks"),
        ],
        [State("modal", "is_open")],
        prevent_initial_call=True,
    )
    def toggle_modal(b1, b2, b3, b4, is_open):
        ctx = callback_context
        if not ctx.triggered:
            return False, "nothing"
        else:
            return True, ctx.triggered[0]["prop_id"].split(".")[0]

    @app.callback(
        [
            Output("view-menu-img", "src"),
            Output("graph-view-container", "style"),
            Output("table-view-container", "style"),
        ],
        [Input("view-menu", "n_clicks")],
        prevent_initial_call=True,
    )
    def toggle_view(vm):
        inv = {"display": "none"}
        vis = {"display": "grid"}
        if vm % 2 == 1:
            return "assets/table_FILL0_wght400_GRAD0_opsz24.svg", inv, vis
        else:
            return "assets/bar_chart_FILL0_wght400_GRAD0_opsz24.svg", vis, inv

    @callback(
        [
            Output(f"open-button-{i + 1}", "style", allow_duplicate=True)
            for i in range(4)
        ]
        + [
            Output(f"filled-container-{i + 1}", "style", allow_duplicate=True)
            for i in range(4)
        ],
        [Input(f"graph-menu-delete-{i + 1}", "n_clicks") for i in range(4)],
        [State(f"open-button-{i + 1}", "style") for i in range(4)]
        + [State(f"filled-container-{i + 1}", "style") for i in range(4)],
        prevent_initial_call=True,
    )
    def delete_graph(g1, g2, g3, g4, vis1, vis2, vis3, vis4, gv1, gv2, gv3, gv4):
        inv = {"display": "none"}
        vis = {"display": "unset"}

        ctx = callback_context
        clicked_btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
        idx = int(clicked_btn_id[-1]) - 1

        button_vis = [vis1, vis2, vis3, vis4]
        graph_vis = [gv1, gv2, gv3, gv4]

        button_vis[idx] = vis
        graph_vis[idx] = inv

        return button_vis + graph_vis

    @callback(
        [
            Output("modal", "is_open", allow_duplicate=True),
            Output("hidden-div", "children", allow_duplicate=True),
        ],
        [Input(f"graph-menu-edit-{i + 1}", "n_clicks") for i in range(4)],
        [],
        prevent_initial_call=True,
    )
    def edit_graph(ic1, ic2, ic3, ic4):
        ctx = callback_context
        clicked_btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
        idx = int(clicked_btn_id[-1]) - 1

        clicks = [ic1, ic2, ic3, ic4]
        clicks[idx] += 1
        return True, "open-button-" + str(idx + 1)
