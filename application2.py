import os
import time
import shutil
import dash
from dash import dcc, html, Input, Output, State, ALL, callback
from banco.dados import Dados
import dash_bootstrap_components as dbc
from config.config import Config
# import dash_auth
from dash import Dash, html, dcc
import hashlib

from config.config import Config

# elements
from sections.sidebar import Sidebar, Sidebar2
from sections.group_menu import ListGroup
from elements.logo import Logo

# login imports
from utils.login_handler import restricted_page
from dash.exceptions import PreventUpdate
from flask_caching import Cache
from flask import Flask, request, redirect, session, url_for
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user

config = Config().config
dados = Dados(config['ambiente'])


# Exposing the Flask Server to enable configuring it for logging in
# Get sectret key in keyword sheet
server = Flask(__name__)
if config['key'] is not None:
    server.secret_key = config['key']

else:
    server.secret_key = os.getenv('SECRET')


@server.route(rule='/login', methods=['POST'])
def login_button_click():
    if request.form:
        email = request.form['username']
        password = request.form['password']
        # password = hashlib.md5((server.secret_key+request.form['password']).encode())

        # Validate User
        try:
            if not email == dados.query_table(
                    table_name='user',
                    # operation='distinct',
                    field_list=[{'name': 'email'}],
                    filter_list=[{'op': 'eq', 'name': 'email', 'value': email}])['email'][0]:
                pass
        except:
            return """invalid username <a href='/login'>login here</a>"""

        # Validate User and Password
        try:
            if password == dados.query_table(
            # if password.hexdigest() == dados.query_table(
                    table_name='user',
                    # operation='distinct',
                    field_list=[{'name': 'password'}],
                    filter_list=[
                        {'op': 'eq', 'name': 'email', 'value': email},
                        {'op': 'eq', 'name': 'password', 'value': password}])['password'][0]:
                        # {'op': 'eq', 'name': 'password', 'value': password.hexdigest()}])['password'][0]:
                pass
        except:
            return """invalid password <a href='/login'>login here</a>"""

        # Create user session
        login_user(User(email))

        session['email'] = email

        if 'url' in session:
            if session['url']:
                url = session['url']
                session['url'] = None
                return redirect(url) ## redirect to target url
        return redirect('/') ## redirect to home


# Inicializao do servidor
app = Dash(
    name=__name__,
    server=server,
    # background_callback_manager=background_callback_manager,
    use_pages=True,
    external_stylesheets=[
        # dbc.themes.LUX,
        # dbc.themes.SPACELAB,
        # dbc.themes.JOURNAL,
        # dbc.themes.SANDSTONE,
        # dbc.themes.LITERA,
        # dbc.themes.YETI,
        dbc.themes.ZEPHYR,
        # dbc.themes.SIMPLEX,
        dbc.icons.BOOTSTRAP,
        # dbc.icons.FONT_AWESOME
    ],
    suppress_callback_exceptions=True,
    external_scripts=['https://cdn.plot.ly/plotly-locale-pt-br-latest.js'],
)
# os.environ['DADOS_VENV'] = f'{dados}'
# os.environ['DADOS_VENV_HEX'] = f'{id(dados)}'

# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
# server.config.update(SECRET_KEY='')

# cache
cache = Cache(
    app=app.server,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory'
    }
)


# For wsgi aws
application = app.server

# VALID_USERNAME_PASSWORD_PAIRS = VALID_USERNAME_PASSWORD
# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD)


# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)


# Layout macro para multi pages
# side_bar = Sidebar2().layout(
#     side_bar_content=[
#
#         # Logo Group
#         # Logo().layout(),
#
#         # Grupo
#         ListGroup().layout2(
#             group_title='',
#             # group_title='Autenticação'.upper(),
#             group_elements=[
#                 # Div para fazer login e encerrar sessão
#                 # html.Div(id="user-status-header"),
#
#             ]
#         ),
#
#     ]
# )


app.layout = dbc.Row(
    id='main_container',
    # class_name='px-0 mx-0 my-1 py-1',
    class_name='m-0 p-0',
    style={
        'background': 'Salmom',
    },
    children=[

        dbc.Row(
            children=[
                dbc.Col(
                    class_name='center-aligned-group-header col-sm-12 col-md-12 col-lg-3 pt-3',
                    children=[
                        Logo().layout(),
                    ],
                ),

                dbc.Col(
                    class_name='center-aligned-group-header col-sm-12 col-md-12 col-lg-9 pt-5 pb-3',
                    children=[
                        dbc.Nav(
                            class_name='center-aligned-group-header',
                            children=[
                                # dbc.NavItem(dbc.NavLink("Home", active=True, href='/GerenciarUsuario')),
                                dbc.DropdownMenu(
                                    children=[
                                        dbc.DropdownMenuItem("Criar", href='/CriarALuno', ),
                                        dbc.DropdownMenuItem("Editar", href='/EditarAluno', ),
                                    ],
                                    label="Aluno",
                                    nav=True,
                                ),
                                dbc.DropdownMenu(
                                    children=[
                                        dbc.DropdownMenuItem("Criar", href='/CriarTurma', ),
                                        dbc.DropdownMenuItem("Editar", href='/EditarTurma', ),
                                        dbc.DropdownMenuItem("Lançar Nota", href='/LancarNotaTurma', ),
                                        dbc.DropdownMenuItem("Avaliação Aluno", href='/StudentEvaluation', ),
                                        dbc.DropdownMenuItem("Lançar Remarks", href='/Remarks', ),
                                        dbc.DropdownMenuItem("Fechar Turma", href='/FecharTurma', ),
                                    ],
                                    label="Turma",
                                    nav=True,
                                ),
                                dbc.DropdownMenu(
                                    children=[
                                        dbc.DropdownMenuItem("Turma p/ Horário", href='/RelatorioTurmaHorario', ),
                                        dbc.DropdownMenuItem('Telefone Alunos', href='/RelatorioTelefoneTurma', ),
                                        dbc.DropdownMenuItem("Etiqueta", href='/RelatorioEtiquetaAluno', ),
                                        dbc.DropdownMenuItem("Nota Turma", href='/RelatorioNotaTurma', ),
                                        dbc.DropdownMenuItem("Boletim Aluno", href='/BoletimAluno', ),
                                        dbc.DropdownMenuItem("Diploma", href='/Diploma', ),
                                    ],
                                    label="Relatório",
                                    nav=True,
                                ),
                                dbc.NavItem(dbc.NavLink("Gerenciar Usuário", active=True, href='/GerenciarUsuario')),
                                dbc.NavItem(dbc.NavLink("Login", active=True, href='/login')),
                                dbc.NavItem(dbc.NavLink("Logout", active=True, href='/logout')),

                            ]
                        ),
                    ],
                ),
            ],
        ),



        dbc.Row(
            id='main_area_app',
            # class_name=' mx-5 px-0 my-0 py-0',
            class_name='px-5 p-0',
            children=[dash.page_container]
        ),

        # dcc.Location(id="url"),

        # Seletores
        # dbc.Row(
        #     id='',
        #     class_name='mx-0 px-0',
        #     children=[
        #         dbc.Row(
        #             children=[
        #                 # dbc.Row(
        #                 #     class_name='col-12',
        #                 #     children=[
        #                 #
        #                 #         dbc.Col(
        #                 #             children=[
        #                 #                 dbc.Col(
        #                 #                     children=[
        #                 #                         dcc.Link(
        #                 #                             style={'font-size': 13},
        #                 #                             children='Login'.upper(),
        #                 #                             href='/login',
        #                 #                             className='justify-content-center text-middle text-center pl-1',
        #                 #                         ),
        #                 #                     ],
        #                 #                 ),
        #                 #                 dbc.Col(
        #                 #                     children=[
        #                 #                         dcc.Link(
        #                 #                             style={'font-size': 13},
        #                 #                             children='Logout'.upper(),
        #                 #                             href='/logout',
        #                 #                             className='justify-content-center text-middle text-center pl-1',
        #                 #                         ),
        #                 #                     ],
        #                 #                 ),
        #                 #             ],
        #                 #         ),
        #                 #         # dbc.Row(side_bar,class_name='justify-content-center'),
        #                 #     ],
        #                 # ),
        #                 dbc.Row(
        #                     class_name='col-12',
        #                     children=[
        #                     ],
        #                 ),
        #             ],
        #         ),
        #         dbc.Row(
        #             children=[
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #                 html.Br(),
        #             ],
        #         )
        #     ],
        # ),

    ],
)


# @app.callback(
#     Output(component_id="user-status-header", component_property="children"),
#     Output(component_id='url', component_property='pathname'),
#     Input(component_id="url", component_property="pathname"),
#     Input(component_id={'index': ALL, 'type': 'redirect'}, component_property='n_intervals')
# )
# def update_authentication_status(path, n):
#     ### logout redirect
#     if n:
#         if not n[0]:
#             return '', dash.no_update
#         else:
#             return '', '/login'
#
#     ### test if user is logged in
#     if current_user.is_authenticated:
#         if path == '/login':
#             return dcc.children="logout".upper(), href="/logout"), ', Link(Nass_name='justify-content-center text-middle text-center', /'
#
#         return dcc.children="logout", href="/logout"), dash.no_upda, Link(Nass_name='justify-content-center text-middle text-center', te
#     else:
#         ### if page is restricted, redirect to login and save path
#         if path in restricted_page:
#             session['url'] = path
#             return dcc.children="login", href="/login"), '/logi, Link(Nass_name='justify-content-center text-middle text-center', n'
#
#     ### if path not login and logout display login link
#     if current_user and path not in ['/login', '/logout']:
#         return dcc.children="login", href="/login"), dash.no_upda, Link(Nass_name='justify-content-center text-middle text-center', te
#
#     ### if path login and logout hide links
#     if path in ['/login', '/logout']:
#         return '', dash.no_update


if __name__ == '__main__':
    # prod
    # application.run(debug=False, port=5000)
    # testes no ec2 do sintegre
    application.run(debug=False, port=5020, host='0.0.0.0')
    # application.run(debug=False, port=5010, host='0.0.0.0')
    # application.run(debug=False, port=5000)
    # app.run_server(debug=False)
