from dash import dcc, callback, Output, Input, State, callback_context, dependencies
import pandas as pd
import plotly.express as px
import data
import os
import os.path as osp

def get_callbacks(app):

    filenames = [filename[:-4] for filename in os.listdir(os.path.dirname(data.__file__)) if filename.endswith('.csv')]

    @app.callback(
        [Output(f"dynamic-sidebar-option-{filename}", 'className') for filename in filenames] \
            + [Output('hidden-div-dataset', 'children'), 
               Output('xaxis-column', 'options'),
               Output('yaxis-column', 'options')],
        [Input(f"dynamic-sidebar-option-{filename}", 'n_clicks') for filename in filenames],
        prevent_initial_call=True
    )
    def update_button_color(*btn_clicks):
        ctx = callback_context
        clicked_btn_id = ctx.triggered[0]['prop_id'].split('.')[0]

        default_style = 'sidebar-option'
        active_style = 'sidebar-option-selected'
        styles = [default_style for _ in range(len(filenames))]

        if clicked_btn_id.rsplit('-', 1)[-1] in filenames:
            clicked_btn_index = filenames.index(clicked_btn_id.rsplit('-', 1)[-1])
            styles[clicked_btn_index] = active_style

        filename = clicked_btn_id.replace('dynamic-sidebar-option-', '') + '.csv'
        fileloc = osp.join(osp.dirname(data.__file__), filename)

        df = pd.read_csv(fileloc)
        options = [{'label': col, 'value': col} for col in df.columns]

        return styles + [filename, options, options]

    
    @callback(
        Output('hidden-div-xdropdown', 'children'),
        Input('xaxis-column', 'value')
    )
    def update_xaxis(col):
        return col

    @callback(
        Output('hidden-div-ydropdown', 'children'),
        Input('yaxis-column', 'value')
    )
    def update_xaxis(col):
        return col

    @callback(
        [Output(component_id='graph-container-1', component_property='children'),
        Output(component_id='graph-container-2', component_property='children'),
        Output(component_id='graph-container-3', component_property='children'),
        Output(component_id='graph-container-4', component_property='children'),
        Output('open-button-1', 'style'),
        Output('open-button-2', 'style'),
        Output('open-button-3', 'style'),
        Output('open-button-4', 'style'),
        Output(component_id='graph-container-1', component_property='style'),
        Output(component_id='graph-container-2', component_property='style'),
        Output(component_id='graph-container-3', component_property='style'),
        Output(component_id='graph-container-4', component_property='style'),
        Output("modal", "is_open", allow_duplicate=True)],
        [Input(component_id='add-graph-button', component_property='n_clicks')],
        [State('hidden-div', 'children'),
        State('hidden-div-xdropdown', 'children'),
        State('hidden-div-ydropdown', 'children'),
        State('open-button-1', 'style'),
        State('open-button-2', 'style'),
        State('open-button-3', 'style'),
        State('open-button-4', 'style'),
        State('graph-container-1', 'children'),
        State('graph-container-2', 'children'),
        State('graph-container-3', 'children'),
        State('graph-container-4', 'children'),
        State('graph-container-1', 'style'),
        State('graph-container-2', 'style'),
        State('graph-container-3', 'style'),
        State('graph-container-4', 'style'),
        State('hidden-div-dataset', 'children')
        ],
        prevent_initial_call=True
        )
    def add_graph(n, btn_id, xcol, ycol, vis1, vis2, vis3, vis4, gc1, gc2, gc3, gc4, gv1, gv2, gv3, gv4, ds):

        graph = dcc.Graph(figure=px.histogram(pd.read_csv(osp.join(osp.dirname(data.__file__), ds)), x=xcol, y=ycol, histfunc='avg'), className='main-graph', \
                            config = {'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'pan', 'select2d', 'lasso2d', 'autoscale']})
        
        inv = {'display': 'none'}
        vis = {'display': 'unset'}
        if btn_id == 'open-button-1':
            return [graph], gc2, gc3, gc4, \
                inv, vis2, vis3, vis4, \
                vis, gv2, gv3, gv4, False
        if btn_id == 'open-button-2':
            return gc1, [graph], gc3, gc4, \
                vis1, inv, vis3, vis4, \
                gv1, vis, gv3, gv4, False
        if btn_id == 'open-button-3':
            return gc1, gc2, [graph], gc4, \
                vis1, vis2, inv, vis4, \
                gv1, gv2, vis, gv4, False
        else:
            return gc1, gc2, gc3, [graph], \
                vis1, vis2, vis3, inv, \
                gv1, gv2, gv3, vis, False

    @app.callback(
        [Output("modal", "is_open", allow_duplicate=True),
        Output('hidden-div', 'children')],
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
            return False, 'nothing'
        else:
            return True, ctx.triggered[0]['prop_id'].split('.')[0]
        