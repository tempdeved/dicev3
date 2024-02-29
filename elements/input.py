import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from elements.element import Component

class Input(Component):

    def __init__(self, id_object: str, title: str, **kwargs):
        super(Input, self).__init__(id_object, title, **kwargs)

    def load(self):

        # Controle dropdown
        self.layout = dbc.Card(
            class_name='shadow-lg border mx-0 my-1 px-0 py-1',
            children=[
                dbc.CardHeader(
                    children=html.P(
                        f'{self.title}'.upper(),
                        className='p-2 m-2',
                    ),
                    class_name='py-0 my-0 justify-content-top text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-0 py-0 my-0',
                    children=[
                        dbc.Input(
                            id=f'{self.id_object}',
                            className='',
                            **self.options
                        )
                    ]
                )
            ]
        )
