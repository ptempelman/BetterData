import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, dash_table, dependencies
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Button("Open Pop-up", id="open-button"),
    dbc.Modal([
        dbc.ModalHeader("Header"),
        dbc.ModalBody("This is the pop-up content."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-button", className="ml-auto")
        ),
    ], id="modal")
])

@app.callback(
    Output("modal", "is_open"),
    [Input("open-button", "n_clicks"), Input("close-button", "n_clicks")],
    [dependencies.State("modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=True)
