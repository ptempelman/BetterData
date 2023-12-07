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
                                id="levelup-message-container",
                                children=[
                                    html.Div(
                                        className="levelup-msg",
                                        children="You leveled up from ",
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
                                    html.Div(
                                        className="levelup-msg",
                                        children="!",
                                    ),
                                ],
                            )
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
