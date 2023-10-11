import dash_bootstrap_components as dbc
from dash import html, dcc


class ListGroup(object):

    def __init__(self):
        ...

    def layout(self, group_title, group_elements):

        layout = dbc.Row(
            children=[
                # dbc.ListGroup(
                #     class_name='text-center',
                #     children=[
                        # html.Br(),
                        html.H5(children=group_title, className='text-center'),
                        # html.H4(children=group_title, className='text-center border-bottom'),
                        dbc.Row(children=group_elements, class_name=''),
                        # html.Hr(),
                        html.Hr(),
                #     ]
                # ),
            ],
        )

        return layout