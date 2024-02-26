import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from elements.element import Component

class DatePicker(Component):

    def __init__(self, id_object: str, title: str, **kwargs):
        super(DatePicker, self).__init__(id_object, title, **kwargs)

    def load(self):

        # Controle dropdown
        self.layout = dbc.Card(
            class_name='shadow-lg border mx-1 my-1 px-1 py-1 text-center',
            # class_name='shadow-lg border mx-0 my-1 px-0 py-1 text-middle text-center',
            children=[
                dbc.CardHeader(
                    children=html.P(
                        f'{self.title}',
                        className='p-2 m-2',
                        style={
                            # 'font-weight': 'bold',
                            'font-size': '14px'
                        }
                    ),
                    class_name='py-0 my-0 justify-content-top text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-0 py-0 my-0',
                    children=[
                        dcc.DatePickerSingle(
                            id=f'{self.id_object}',
                            className='',
                            **self.options
                        )
                    ]
                )
            ]
        )


class DatePickerRange(Component):

    def __init__(self, id_object: str, title: str, **kwargs):
        super(DatePickerRange, self).__init__(id_object, title, **kwargs)

    def load(self):

        # Controle dropdown
        self.layout = dbc.Card(
            class_name='shadow-lg border mx-1 my-1 px-1 py-1 text-center',
            # class_name='shadow-lg border mx-0 my-1 px-0 py-1 text-middle text-center',
            children=[
                dbc.CardHeader(
                    children=html.P(f'{self.title}'),
                    class_name='py-0 my-0 justify-content-top text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-0 py-0 my-0',
                    children=[
                        dcc.DatePickerRange(
                            id=f'{self.id_object}',
                            className='',
                            **self.options
                        )
                    ]
                )
            ]
        )

