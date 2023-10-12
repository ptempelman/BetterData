from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import os.path as osp
import io
import base64

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div(style={'height': '100vh', 'margin': '0', 'width': '100vw'}, children=[
    # New vertical column div on the left
    html.Div(style={'backgroundColor': 'black', 'width': '100px', 'height': '100%', 'position': 'fixed'}, children=[
        html.Button("+", id="upload-button", style={'marginTop': '20px', 'marginLeft': '35px', 'background': 'white'}),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '90%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '20px auto',
                'display': 'none'  # Initially hidden
            },
            multiple=False
        ),
    ]),

    # The rest of your layout
    html.Div(style={'marginLeft': '110px'}, children=[
        html.Div(children=[
            html.Img(src='/assets/sigma_logo.jpeg', id='overlay-image1', 
                     style={'margin-top': '3px', 'margin-left': '10px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #ffffff'}),
            
            html.Img(src='/assets/john_face.png', id='overlay-image2', 
                     style={'margin-top': '3px', 'margin-left': '10px', 'width': '30px', 'height': '30px', 'border-radius': '50%', 'border': '2px solid #00b7ff'})
        ],
        style={'textAlign': 'left', 'color': 'blue', 'fontSize': 30, 'background-color': 'black', 
               'padding': 0, 'width': '100%', 'height': '40px'}),

        html.Div(className='row', children=[
            dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                           value='lifeExp',
                           inline=True,
                           id='my-radio-buttons-final')
        ]),

        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'}, id='table')
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='histo-chart-final')
            ])
        ])
    ])
])

@app.callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

@app.callback(Output('upload-data', 'style'),
              Input('upload-button', 'n_clicks'))
def show_upload(n_clicks):
    if n_clicks and n_clicks > 0:
        return {'display': 'block'}
    return {'display': 'none'}

@app.callback(Output('table', 'data'),
              [Input('upload-data', 'contents')])
def upload_file(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        global df
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df.to_dict('records')
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
