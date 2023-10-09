from dash import html, dcc
import dash_bootstrap_components as dbc



class Titulo(object):

    def __init__(self):
        ...


    def load(self, id, title_name):

        # Titulo da pagina
        layout = dbc.Row(
            id=id,
            class_name='px-0 mx-0 justify-content-center text text-center',
            children=[
                dbc.Row(
                    id=f'{id}_title_row',
                    children=[
                        html.H1(
                            children=[title_name],
                            className='py-3 px-0 mx-0')
                    ]
                )
            ],
        ),


        return layout[0]
