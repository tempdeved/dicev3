import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from elements.element import Component

class RadioItem(Component):

    def __init__(self, id_object: str, title: str, **kwargs):
        super(RadioItem, self).__init__(id_object, title, **kwargs)

    def load(self):

        # Controle dropdown
        self.layout = dbc.Card(
            class_name='shadow-lg border mx-1 my-1 px-1 py-1',
            children=[
                dbc.CardHeader(
                    children=html.P(f'{self.title}'),
                    class_name='py-0 my-0 justify-content-middle text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-2 py-0 my-2 justify-content-center',
                    children=[
                        dbc.Row(
                            class_name='justify-content-center text-middle text-center',
                            children=[
                                dbc.RadioItems(
                                    id=f'{self.id_object}',
                                    **self.options
                                )
                            ]
                        ),
                    ]
                )
            ]
        )



class CheckList(Component):

    def __init__(self, id_object: str, title: str, **kwargs):
        super(CheckList, self).__init__(id_object, title, **kwargs)

    def load(self):

        # Controle dropdown
        self.layout = dbc.Card(
            class_name='shadow-lg border mx-1 my-1 px-1 py-1',
            children=[
                dbc.CardHeader(
                    children=html.P(f'{self.title}'),
                    class_name='py-0 my-0 justify-content-middle text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-2 py-0 my-2 justify-content-center',
                    children=[
                        dbc.Row(
                            class_name='justify-content-center text-middle text-center',
                            children=[
                                dbc.Checklist(
                                    id=f'{self.id_object}',
                                    **self.options
                                )
                            ]
                        ),
                    ]
                )
            ]
        )
