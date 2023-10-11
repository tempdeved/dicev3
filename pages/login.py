import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
# login libs
from flask_login import current_user

dash.register_page(__name__)
page_name = __name__[6:].replace('.', '_')


# Login screen
def layout():

    inputs = dbc.Row(
        class_name='justify-content-center mx-0 py-0',
        children=[
            # username
            dbc.Row(
                class_name='justify-content-center mx-0 py-0',
                children=[
                    dbc.Col(
                        class_name='col-12 col-lg-4',
                        children=[
                            dbc.Input(
                                id="uname-box",
                                placeholder="Enter your email",
                                type="text",
                                name='username',
                                size='sm',
                                class_name='my-1'
                            ),
                        ]
                    )
                ]
            ),

            #password
            dbc.Row(
                class_name='justify-content-center mx-0 py-0 pb-2',
                children=[
                    dbc.Col(
                        class_name='col-12 col-lg-4',
                        children=[
                            dbc.Input(
                                id="pwd-box",
                                placeholder="Enter your password",
                                type="password",
                                name='password',
                                size='sm',
                                class_name='my-1'
                            ),
                        ]
                    )
                ]
            ),

            # row de botoes
            dbc.Row(
                class_name='justify-content-center mx-0 py-2',
                # class_name='justify-content-center my-2',
                children=[
                    dbc.Col(
                        class_name='col-12 col-lg-2 d-grid gap-2',
                        # class_name='col-12 col-lg-8',
                        children=[
                            dbc.Button(
                                id="login-button",
                                children="Login",
                                n_clicks=0,
                                type="submit",
                            ),
                            html.Div(
                                id="output-state",
                                children="",
                            )
                        ]
                    )
                ]
            )
        ]
    )

    input_social = dbc.Row(
        class_name='justify-content-start my-2',
        children=[
                    dbc.Col(
                        class_name='col-12 col-lg-3 d-grid gap-2',
                        children=[
                            dbc.Button(
                                id=f"login-microsoft_{page_name}",
                                children=' Log in com Microsoft',
                                n_clicks=0,
                                type="submit",
                                class_name='bi bi-microsoft',
                            ),
                        ]
                    )
                ]
    )

    # linha_separatoria = dbc.Row(
    #     class_name='justify-content-center mx-0 py-0',
    #     children=[
    #         dbc.Col(width=15, children=html.Hr()),
    #         # dbc.Col(width=2, children=html.P('ou'), class_name='text-center'),
    #         # dbc.Col(width=5, children=html.Hr())
    #     ]
    # ),

    formulario = html.Form(
        id=f'form_cadastro_{page_name}',
        className='mx-0 my-4',
        # class_name='mx-2 my-2',
        method='POST',
        children=[
            dbc.Row(html.H2(children="Login", className='text-center py-2')),
            dbc.Row(inputs),
            # dbc.Row(linha_separatoria),
            # dbc.Row(input_social),
        ]
    )

    layout = dbc.Container(
        children=dbc.Card(
            children=formulario,
            class_name='shadow-lg'
        ),
        # class_name='my-10 py-10'
    )



    # layout = dbc.Row(
    #     id=f'main_container_{page_name}',
    #     class_name='mx-0 px-0',
    #     children=[
    #         html.Form(
    #             method='POST',
    #             children=[
    #                 html.H2("Please log in to continue:", id="h1"),
    #                 dbc.Input(placeholder="Enter your username", type="text", id="uname-box", name='username', size='md'),
    #                 dbc.Input(placeholder="Enter your password", type="password", id="pwd-box", name='password', size='md'),
    #                 dbc.Button(children="Login", n_clicks=0, type="submit", id="login-button"),
    #                 html.Div(children="", id="output-state")
    #             ],
    #         )
    #     ]
    # )


    return layout