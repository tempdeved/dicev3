import dash_bootstrap_components as dbc
import dash
from dash import Dash, dcc, html, Input, Output, callback_context, callback, State



class Sidebar(object):
    def __init__(self):
        pass

    def layout(self, side_bar_content: list = []):

        layout = dbc.Row(
            class_name='py-0 px-0 mx-0 my-0',
            children=[

                dbc.Row(
                    id='',
                    class_name='px-0 px-md-2 mx-0 py-2 justify-content-center',
                    children=[
                        dbc.Col(
                            class_name='col-2 col-lg-1 px-0 mx-0 d-block '
                                       'justify-content-center text-center',
                            children=[  
                                html.P('Menu', className='text-center px-0 mx-0 py-0 my-0'),

                                dbc.Button(
                                    title='Menu',
                                    id='open-offcanvas',
                                    color='primary',
                                    outline=False,
                                    n_clicks=0,
                                    class_name='bi bi-three-dots fas fa-bi-three-dots-lg '
                                               'justify-content-center text-center mx-0 px-0 '
                                               'opacity-75 btn-sm text-align-center w-100 w-lg-50',
                                ),
                            ]
                        ),
                    ]
                ),

                dbc.Offcanvas(
                    children=side_bar_content,
                    id="offcanvas",
                    title="Menu",
                    is_open=False,
                    class_name='bg-white d-block justify-content-center justify-content-middle text-center px-0 '
                               'overflow-auto'
                ),
            ]
        )
        return layout

@callback(
    Output(component_id="offcanvas", component_property="is_open"),
    Input(component_id="open-offcanvas", component_property="n_clicks"),
    [State(component_id="offcanvas", component_property="is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open