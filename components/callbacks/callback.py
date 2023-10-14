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
from components.callbacks.container_components import get_graph, get_table
from components.content.dashboard_item import render_dashboard_item
import data
import os
import os.path as osp
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import html
import dash_bootstrap_components as dbc
import dash_draggable


def get_callbacks(app):
    filenames = [
        filename[:-4]
        for filename in os.listdir(os.path.dirname(data.__file__))
        if filename.endswith(".csv")
    ]

    @app.callback(
        [
            Output("xaxis-column", "options"),
            Output("yaxis-column", "options"),
        ],
        Input("hidden-div-dataset", "children"),
        prevent_initial_call=True,
    )
    def update_columns(filename):
        if not filename:
            return no_update
        fileloc = osp.join(osp.dirname(data.__file__), filename)

        df = pd.read_csv(fileloc)
        options = [{"label": col, "value": col} for col in df.columns]
        return options, options

    @app.callback(
        [
            Output("hidden-div-dataset", "children", allow_duplicate=True),
        ],
        Input("dataset-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_dataset(filename):
        if not filename:
            return no_update

        return [filename]
    
    @app.callback(
        [
            Output("hidden-div-dataset", "children", allow_duplicate=True),
        ],
        Input("dataset-dropdown-table", "value"),
        prevent_initial_call=True,
    )
    def update_dataset(filename):
        if not filename:
            return no_update

        return [filename]

    # # @app.callback(
    # #     [
    # #         Output(f"dynamic-sidebar-option-{filename}", "className")
    # #         for filename in filenames
    # #     ]
    # #     + [
    # #         Output("hidden-div-dataset", "children"),
    # #         Output("xaxis-column", "options"),
    # #         Output("yaxis-column", "options"),
    # #         Output("table-view-container", "children"),
    # #     ],
    # #     [
    # #         Input(f"dynamic-sidebar-option-{filename}", "n_clicks")
    # #         for filename in filenames
    # #     ],
    # #     prevent_initial_call=True,
    # # )
    # # def update_button_color(*btn_clicks):
    # #     ctx = callback_context
    # #     clicked_btn_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # #     default_style = "sidebar-option"
    # #     active_style = "sidebar-option-selected"
    # #     styles = [default_style for _ in range(len(filenames))]

    # #     if clicked_btn_id.rsplit("-", 1)[-1] in filenames:
    # #         clicked_btn_index = filenames.index(clicked_btn_id.rsplit("-", 1)[-1])
    # #         styles[clicked_btn_index] = active_style

    # #     filename = clicked_btn_id.replace("dynamic-sidebar-option-", "") + ".csv"
    # #     fileloc = osp.join(osp.dirname(data.__file__), filename)

    # #     df = pd.read_csv(fileloc)
    # #     options = [{"label": col, "value": col} for col in df.columns]

    # #     table_view = dash_table.DataTable(
    # #         id="table",
    # #         columns=[{"name": i, "id": i} for i in df.columns],
    # #         data=df.to_dict("records"),
    # #         style_header={
    # #             "color": "white",
    # #             "background-color": "#7d7d7d",
    # #             "border": "1px solid black",
    # #         },
    # #         style_cell={"border": "1px solid grey"},
    # #     )

    # #     return styles + [filename, options, options, [table_view]]

    @callback(
        Output("hidden-div-xdropdown", "children"),
        Input("xaxis-column", "value"),
        prevent_initial_call=True,
    )
    def update_xaxis(col):
        return col

    @callback(
        Output("hidden-div-ydropdown", "children"),
        Input("yaxis-column", "value"),
        prevent_initial_call=True,
    )
    def update_yaxis(col):
        return col

    @callback(
        Output("hidden-div-graph-type", "children"),
        Input("graph-type-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_graph_type(graph_type):
        return graph_type

    @callback(
        Output("modal", "is_open", allow_duplicate=True),
        Input({"type": "add-graph-button", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def close_modal(n):
        if n is None or n[-1] <= 0:
            return no_update
        print("modal closed")
        return False

    @callback(
        [
            Output("modal", "is_open", allow_duplicate=True),
            Output("total-modal-clicks", "children", allow_duplicate=True),
        ],
        Input({"type": "open-button", "index": ALL}, "n_clicks"),
        State("total-modal-clicks", "children"),
        prevent_initial_call=True,
    )
    def open_modal(n_clicks, total_clicks):
        print(
            "trying to open modal with clicks:", n_clicks, " and total:", total_clicks
        )
        total_clicks = int(total_clicks)
        if n_clicks is None or sum(n_clicks) != total_clicks + 1:
            return no_update
        print(f"modal opened\n")
        return True, total_clicks + 1

    @callback(
        [
            Output(
                {"type": "graph-container", "index": MATCH},
                "children",
                allow_duplicate=True,
            ),
            Output(
                {"type": "open-button", "index": MATCH}, "style", allow_duplicate=True
            ),
            Output(
                {"type": "filled-container", "index": MATCH},
                "style",
                allow_duplicate=True,
            ),
        ],
        [Input({"type": "add-graph-button", "index": MATCH}, "n_clicks")],
        [
            State("container-fill-type", "children"),
            State("hidden-div-xdropdown", "children"),
            State("hidden-div-ydropdown", "children"),
            State("hidden-div-graph-type", "children"),
            State("hidden-div-dataset", "children"),
        ],
        prevent_initial_call=True,
    )
    def add_component(
        n,
        container_fill_type,
        xcol,
        ycol,
        graph_type,
        ds,
    ):
        print("trying to add graph with clicks:", n)
        if n is None or n <= 0:
            return no_update
        
        ctx = callback_context

        if container_fill_type == 0:
            component = get_graph(ctx, ds, graph_type, xcol, ycol)
        # elif container_fill_type == 0:
        else:
            component = get_table(ds)
            
            
        inv = {"display": "none"}
        vis = {"display": "unset"}

        return component, inv, vis

    @app.callback(
        [
            Output("draggable", "children", allow_duplicate=True),
            Output("hidden-div-new-container-index", "children"),
        ],
        Input({"type": "add-graph-button", "index": ALL}, "n_clicks"),
        [
            State("hidden-div-new-container-index", "children"),
            State("draggable", "children"),
        ],
        prevent_initial_call=True,
    )
    def visualize_empty_container(n_clicks, container_index, dc):
        if n_clicks is None or n_clicks[-1] <= 0:
            return no_update

        container_index = container_index[0] + 1

        dc.append(render_dashboard_item(container_index))
        print(f"updated container index: {container_index}")

        return dc, [container_index]

    @app.callback(
        Output("modal", "children"),
        Input({"type": "open-button", "index": ALL}, "n_clicks"),
        [State("total-modal-clicks", "children"), State("modal", "children")],
        prevent_initial_call=True,
    )
    def update_modal_footer_button(n_clicks, total_clicks, mc):
        total_clicks = int(total_clicks)
        print(
            f"trying to update modal footer with {n_clicks} == {total_clicks}",
            sum(n_clicks) == total_clicks,
        )
        if n_clicks is None or sum(n_clicks) != total_clicks + 1:
            return no_update

        ctx = callback_context
        print(
            f"updated modal footer button {ctx.triggered[0]['prop_id'].split('.')[0]}"
        )
        idx = int(ctx.triggered[0]["prop_id"].split(".")[0].split(":")[1][0])

        mc[-1] = dbc.ModalFooter(
            dbc.Button(
                "Add",
                id={"type": "add-graph-button", "index": idx},
                className="ml-auto",
                n_clicks=0,
            )
        )

        return mc

    # @app.callback(
    #     [
    #         Output("view-menu-img", "src"),
    #         Output("graph-view-container", "style"),
    #         Output("table-view-container", "style"),
    #     ],
    #     [Input("view-menu", "n_clicks")],
    #     prevent_initial_call=True,
    # )
    # def toggle_view(vm):
    #     inv = {"display": "none"}
    #     vis = {"display": "grid"}
    #     if vm % 2 == 1:
    #         return "assets/table_FILL0_wght400_GRAD0_opsz24.svg", inv, vis
    #     else:
    #         return "assets/bar_chart_FILL0_wght400_GRAD0_opsz24.svg", vis, inv

    @callback(
        [
            Output(
                {"type": "open-button", "index": MATCH}, "style", allow_duplicate=True
            ),
            Output(
                {"type": "filled-container", "index": MATCH},
                "style",
                allow_duplicate=True,
            ),
        ],
        Input({"type": "graph-menu-delete", "index": MATCH}, "n_clicks"),
        prevent_initial_call=True,
    )
    def delete_graph(n_clicks):
        if n_clicks is None or n_clicks <= 0:
            return no_update

        print("graph deleted")
        inv = {"display": "none"}
        vis = {"display": "unset"}
        return vis, inv

    @callback(
        Output({"type": "open-button", "index": MATCH}, "n_clicks"),
        Input({"type": "graph-menu-edit", "index": MATCH}, "n_clicks"),
        State({"type": "open-button", "index": MATCH}, "n_clicks"),
        prevent_initial_call=True,
    )
    def edit_graph_open_button_clicks(n_clicks, graph_clicks):
        print(f"trying to manipulate graph button after edit with clicks {n_clicks}")

        if n_clicks is None:
            return no_update

        print(f"manipulating addgraphbutton clicks after edit to {graph_clicks + 1}")

        return graph_clicks + 1

    # @app.callback(
    #     [
    #         Output("draggable", "children", allow_duplicate=True),
    #         Output("total-edit-clicks", "children")
    #     ],
    #     Input({"type": "graph-menu-edit", "index": ALL}, "n_clicks"),
    #     [
    #         State("draggable", "children"),
    #         State("total-edit-clicks", "children")
    #     ],
    #     prevent_initial_call=True,
    # )
    # def take_away_extra_container(n_clicks, dc, total_edit_clicks):
    #     print("trying to remove extra container with clicks", n_clicks)
    #     n_clicks = [0 if x is None else x for x in n_clicks]
    #     if n_clicks is None or sum(n_clicks) != total_edit_clicks + 1:
    #         return no_update

    #     print("removing extra container")

    #     dc.pop()
    #     return dc, total_edit_clicks + 1

    @app.callback(
        [
            Output({"type": "menu-type", "index": ALL}, "style"),
            Output("container-fill-type", "children"),
            Output("menu-switch-clicks", "children"),
        ],
        Input({"type": "add-menu-type", "index": ALL}, "n_clicks"),
        State("menu-switch-clicks", "children")
    )
    def switch_menus(n_clicks, total_clicks):
        print("trying to switch menus with", n_clicks)
        n_clicks = [0 if x == None else x for x in n_clicks]
        if n_clicks is None or sum(n_clicks) != total_clicks + 1:
            return no_update

        print("switching menus")
        ctx = callback_context
        idx = int(ctx.triggered[0]["prop_id"].split(".")[0].split(":")[1][0])

        inv = {"display": "none"}
        vis = {"display": "unset"}

        menu_visibilities = [inv] * len(n_clicks)
        menu_visibilities[idx] = vis

        return menu_visibilities, idx, total_clicks + 1

    # @app.callback(
    #     Output({"type": "menu-type", "index": MATCH}, "style"),
    #     Input({"type": "add-menu-type", "index": MATCH}, "n_clicks"),
    # )
    # def switch_menus():
    #     vis = {"display": "unset"}
    #     return vis
