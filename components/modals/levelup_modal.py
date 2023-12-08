from dash import html, dcc
import dash_bootstrap_components as dbc
import os


def render_levelup_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(children="Level up!"),
            dbc.ModalBody(
                children=[
                    html.Div(
                        id="levelup-modal-body",
                        children=[
                            html.Div(
                                className="levelup-message-container",
                                children=[
                                    html.Div(
                                        className="levelup-msg",
                                        children="Level up! From ",
                                    ),
                                    html.Div(
                                        id="old-user-level",
                                        className="levelup-msg levelup-msg-level-from",
                                        children="Novice",
                                    ),
                                    html.Div(
                                        children=" to ",
                                        className="levelup-msg",
                                    ),
                                    html.Div(
                                        id="new-user-level",
                                        className="levelup-msg levelup-msg-level-to",
                                        children="Novice",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="levelup-message-container",
                                children=[
                                    html.Div(
                                        className="levelup-msg",
                                        children="You unlocked: ",
                                    ),
                                ],
                            ),
                            html.Img(
                                id="levelup-functionality-image",
                                src="assets/master.png",
                                style={
                                    "height": "auto",
                                    "width": "90%",
                                    "margin": "5%",
                                },
                            ),
                        ],
                    )
                ],
            ),
            dbc.ModalFooter(),
        ],
        id="levelup-modal",
        is_open=False,
        backdrop=True,
        centered=True,
    )
