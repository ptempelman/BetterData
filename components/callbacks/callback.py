from dash import dcc, callback, Output, Input, State, callback_context
import plotly.express as px

def get_callbacks(app, df):

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
        ],
        prevent_initial_call=True
        )
    def add_graph(n, btn_id, xcol, ycol, vis1, vis2, vis3, vis4, gc1, gc2, gc3, gc4, gv1, gv2, gv3, gv4):

        graph = dcc.Graph(figure=px.histogram(df, x=xcol, y=ycol, histfunc='avg'), className='main-graph', \
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
        