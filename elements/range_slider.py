import dash_bootstrap_components as dbc
from dash import dcc, html

from elements.element import Component

class RangeSlider(Component):

    def __init__(self, id_object: str, title: str, **kwargs):
        super(RangeSlider, self).__init__(id_object, title, **kwargs)



    def load(self):

        self.layout = dbc.Card(
            class_name='shadow-lg border mx-0 my-1 px-0 py-1',
            children=[
                dbc.CardHeader(
                    children=html.P(f'{self.title}'),
                    class_name='py-0 my-0 justify-content-top text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-0 py-0 my-2',
                    children=[
                        dcc.RangeSlider(
                            id=f'{self.id_object}',
                            className='',
                            **self.options
                        )
                    ]
                )
            ]
        )



