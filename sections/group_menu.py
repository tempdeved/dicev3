import dash_bootstrap_components as dbc
from dash import html, dcc


class ListGroup(object):

    def __init__(self):
        ...

    def layout(self, group_title, group_elements):

        layout = dbc.Row(
            children=[
                dbc.ListGroup(
                    class_name='py-2, text-center',
                    children=[
                        html.H4(children=group_title, className='text-center'),
                        # html.H4(children=group_title, className='text-center border-bottom'),
                        dbc.Row(children=group_elements),
                        # html.Hr(),
                        html.Br(),
                    ]
                ),
            ],
        )

        return layout