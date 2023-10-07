from dash import html
import dash_bootstrap_components as dbc

def render_topbar():
    return html.Div(className='top-bar', children=[

        html.Div(style={'height': '100%', 'width': '300px', 'display': 'flex'}, children=[
            html.Button(style={'marginLeft': '30px'},
                children=[
                    html.Img(src='/assets/sigma_logo.jpeg', id='overlay-image1', 
                        style={'marginTop': '0px', 'marginLeft': '0px', 'width': '30px', 'height': '30px', 'borderRadius': '50%', 'border': '2px solid #ffffff'}),
                ],
                className='square-button'
            ),
            html.Div(
                children=[
                    html.Img(src='/assets/john_face.png', id='overlay-image2', 
                        style={'marginTop': '0px', 'marginLeft': '0px', 'width': '30px', 'height': '30px', 'borderRadius': '50%', 'border': '2px solid #00b7ff'})
                ],
                className='square-button'
            ),

            html.Div(
                children=[
                    dbc.Button('+', className='btn-lg, plus'),
                ],
                className='square-button'
            ),
        ]),

        html.Button('SIGN IN', className='login-button')
    ])
