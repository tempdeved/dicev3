import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash import Input, Output, State, html, callback


class Logo(object):

    def __init__(self):
        pass

    def layout(self):

        layout = dbc.Row(
            class_name='justify-content-center',
            children=[
                html.A(children=[
                    html.Img(
                        src="/static/images/logo/logo.webp",
                        alt='logo',
                        className='perfil_avatar py-2 mx-auto text-center',
                        style={'height': '100%', 'width': '50%'},

                    ),
                ], href='/'),
                # html.Hr()
            ],
        )

        return layout