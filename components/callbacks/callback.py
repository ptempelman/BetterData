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
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from components.callbacks.api_calls import get_generated_graph
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


def check_levelup(exp, cur_level):
    new_level = cur_level
    if (
        (exp < 100 and exp + 40 >= 100)
        or (exp < 250 and exp + 40 >= 250)
        or (exp < 400 and exp + 40 >= 400)
    ):
        if exp + 40 >= 100:
            new_level = "Contributor"
        if exp + 40 >= 250:
            new_level = "Master"
        if exp + 40 >= 400:
            new_level = "Grandmaster"
        return True, new_level
    return False, new_level


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
            Output("dropdown-hovername-hist", "options"),
            Output("dropdown-color-hist", "options"),
            Output("dropdown-size", "options"),
            Output("dropdown-color", "options"),
            Output("dropdown-hovername", "options"),
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
        return options, options, options, options, options, options, options

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

    @app.callback(
        [
            Output("hidden-div-dataset", "children", allow_duplicate=True),
        ],
        Input("dataset-dropdown-ai", "value"),
        prevent_initial_call=True,
    )
    def update_dataset(filename):
        if not filename:
            return no_update

        return [filename]

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
        [
            Output("hidden-div-graph-type", "children"),
            Output("advanced-scatter-options", "style"),
            Output("advanced-histogram-options", "style"),
        ],
        Input("graph-type-dropdown", "value"),
        State("user-experience", "children"),
        prevent_initial_call=True,
    )
    def update_graph_type(graph_type, exp):
        print(f"Updated graph type with {graph_type}")

        inv = {"display": "none"}
        vis = {"display": "flex"}
        advanced_menus_vis = inv, inv
        if graph_type == "scatterplot" and exp >= 250:
            advanced_menus_vis = vis, inv
        elif graph_type == "histogram" and exp >= 250:
            advanced_menus_vis = inv, vis
        return graph_type, *advanced_menus_vis

    @callback(
        Output("hidden-div-size", "children", allow_duplicate=True),
        Input("dropdown-size", "value"),
        prevent_initial_call=True,
    )
    def update_size(size):
        print(f"Updated size with {size}")
        return size

    @callback(
        Output("hidden-div-color", "children", allow_duplicate=True),
        Input("dropdown-color", "value"),
        prevent_initial_call=True,
    )
    def update_color(color):
        print(f"Updated color with {color}")
        return color

    @callback(
        Output("hidden-div-hovername", "children", allow_duplicate=True),
        Input("dropdown-hovername", "value"),
        prevent_initial_call=True,
    )
    def update_hovername(hovername):
        print(f"Updated hovername with {hovername}")
        return hovername

    @callback(
        Output("hidden-div-color", "children", allow_duplicate=True),
        Input("dropdown-color-hist", "value"),
        prevent_initial_call=True,
    )
    def update_color(color):
        print(f"Updated color with {color}")
        return color

    @callback(
        Output("hidden-div-hovername", "children", allow_duplicate=True),
        Input("dropdown-hovername-hist", "value"),
        prevent_initial_call=True,
    )
    def update_hovername(hovername):
        print(f"Updated hovername with {hovername}")
        return hovername

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
            Output("graph-type-dropdown", "style"),
            Output({"type": "add-menu-type", "index": 1}, "style"),
            Output({"type": "add-menu-type", "index": 2}, "style"),
        ],
        Input({"type": "open-button", "index": ALL}, "n_clicks"),
        [State("total-modal-clicks", "children"), State("user-experience", "children")],
        prevent_initial_call=True,
    )
    def open_modal(n_clicks, total_clicks, exp):
        print(
            "trying to open modal with clicks:", n_clicks, " and total:", total_clicks
        )
        total_clicks = int(total_clicks)
        if n_clicks is None or sum(n_clicks) != total_clicks + 1:
            return no_update
        print(f"modal opened\n")

        inv = {"display": "none"}
        vis = {"display": "block"}
        contributor_vis = inv
        master_vis = inv
        print(exp)
        if int(exp) >= 100:
            contributor_vis = vis
        if int(exp) >= 400:
            master_vis = vis

        return (True, total_clicks + 1, contributor_vis, contributor_vis, master_vis)

    @callback(
        Output("hidden-div-graph-prompt", "children"), Input("input-prompt-ai", "value")
    )
    def update_prompt(prompt):
        return prompt

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
            State("hidden-div-size", "children"),
            State("hidden-div-color", "children"),
            State("hidden-div-hovername", "children"),
            State("hidden-div-graph-prompt", "children"),
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
        size,
        color,
        hovername,
        prompt,
    ):
        print("trying to add graph with clicks:", n)
        if n is None or n <= 0:
            return no_update

        ctx = callback_context

        print(ds)

        df = pd.read_csv(osp.join(osp.dirname(data.__file__), ds))
        if container_fill_type == 0:
            component = get_graph(
                ctx, df, graph_type, xcol, ycol, size, color, hovername
            )
        elif container_fill_type == 1:
            component = get_table(ds)
        else:
            with open("openai_api_key.txt", "r", encoding="utf-8") as file:
                api_key: str = file.read()
                pred = get_generated_graph(
                    api_key=api_key,
                    df=df,
                    prompt=prompt,
                )
            pred = f"graph = {pred}"
            print(pred)
            namespace = {"df": df, "dcc": dcc, "go": go, "px": px}

            exec(pred, namespace)
            component = namespace["graph"]

        inv = {"display": "none"}
        vis = {"display": "unset"}

        return component, inv, vis

    @callback(
        [
            Output("user-experience", "children"),
            Output("levelup-modal", "is_open"),
            Output("old-user-level", "children"),
            Output("new-user-level", "children"),
            Output("levelup-functionality-image", "src"),
        ],
        [Input({"type": "add-graph-button", "index": ALL}, "n_clicks")],
        [
            State("user-experience", "children"),
            State("new-user-level", "children"),
        ],
        prevent_initial_call=True,
    )
    def check_levelup_after_add(n, exp, cur_level):
        print("checking levelup", n)
        if n is None or n[0] <= 0:
            return no_update

        levelup, new_level = check_levelup(exp, cur_level)
        image_src = f"assets/{new_level.lower()}.png"
        return exp + 40, levelup, cur_level, new_level, image_src

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
        State("menu-switch-clicks", "children"),
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
