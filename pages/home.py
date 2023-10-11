
import dash
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
from elements.titulo import Titulo
from dash import html, dcc, dash_table, callback, Input, Output, State
from pages.login import layout as login_layout
from flask_login import current_user
from utils.login_handler import require_login
from flask import Flask, request, redirect, session, url_for

from banco.dados import Dados
from config.config import Config

page_name = __name__[6:].replace('.', '_')
dash.register_page(__name__, path=f'/')
# require_login(__name__)

content_layout = dbc.Row(
    id=f'main-container-{page_name}',
    # class_name='px-2 mx-0 shadow-lg',
    children=[
        dbc.Row(id=f'first-load-{page_name}'),
    ],
    className='m-0 p-0'
)

def layout():
    try:
        if current_user.is_authenticated:
            return content_layout
    except Exception as err:

        result = dbc.Row(
            id=f'main-container-{page_name}',
            # class_name='px-2 mx-0 shadow-lg',
            children=[
                dbc.Row(id=f'first-load-{page_name}'),
            ],
            className='m-0 p-0'
        )

        return result
    result = dbc.Row(
        id=f'main-container-{page_name}',
        # class_name='px-2 mx-0 shadow-lg',
        children=[
            dbc.Row(id=f'first-load-{page_name}'),
        ],
        className='m-0 p-0'
    )

    return result


@callback(
    Output(component_id=f'first-load-{page_name}', component_property='children'),
    Input(component_id=f'main-container-{page_name}', component_property='children')
)
def def_welcome_msg(m_container):

    config = Config().config
    dados = Dados(config['ambiente'])

    try:

        if session['email'] == 'logout' or session['email'] == '':
            raise ValueError

        user_email = session['email']

        df_func  = dados.query_table(
            table_name='funcionario',
            # field_list=[
            #     {'name': 'email'},
            #     {'name': 'status'},
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'email_func', 'value': user_email}
            ]
        )

        nome_completo = df_func['nome_completo'][0]
        tipo = df_func['tipo'][0]
        msg = f'{nome_completo} - {tipo}'
        result = dbc.Row(
            children=[
                dbc.Row(f'Seja bem vindo!', className='justify-content-center'),
                dbc.Row(Titulo().load(id=f'titulo-pagina-{page_name}', title_name=msg)),
            ],className='justify-content-center m-0 p-0'
        )
    except:
        result = dbc.Row(
            children=[
                'Seja bem vindo! faça login para acessar os recursos do sistema'
            ],
            className='justify-content-center m-0 p-0'
        )

    return result






