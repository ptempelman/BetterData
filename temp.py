import dash
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Button("+", id="plus-button", style={"fontSize": "24px"}),
    
    dbc.Modal(
        [
            dbc.ModalHeader("Popup Menu"),
            dbc.ModalBody("Complete the content here..."),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal-button", className="ml-auto")
            ),
        ],
        id="popup-menu",
    ),
])

@app.callback(
    Output("popup-menu", "is_open", allow_duplicate=True),
    Input("plus-button", "n_clicks"),
    prevent_initial_call=True
)
def show_popup(n):
    return True

@app.callback(
    [Output("plus-button", "style"),
     Output("popup-menu", "is_open", allow_duplicate=True)],  # This line is added
    Input("close-modal-button", "n_clicks"),
    prevent_initial_call=True
)
def hide_plus_button_and_popup(n):
    return [{"display": "none"}, False]  # This line is modified

if __name__ == '__main__':
    app.run_server(debug=True)
