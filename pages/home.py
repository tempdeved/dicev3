import datetime

import dash
import pandas as pd
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
from elements.titulo import Titulo
from dash import html, dcc, dash_table, callback, Input, Output, State
from pages.login import layout as login_layout
from flask_login import current_user
from utils.login_handler import require_login
from flask import Flask, request, redirect, session, url_for
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import random
import datetime
from banco.dados import Dados
from config.config import Config

page_name = __name__[6:].replace('.', '_')
dash.register_page(__name__, path=f'/')
# require_login(__name__)

config = Config().config
dados = Dados(config['ambiente'])

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

    try:

        if session['email'] == 'logout' or session['email'] == '':
            raise ValueError

        user_email = session['email']

        df_func  = dados.query_table(
            table_name='funcionario',
            filter_list=[
                {'op': 'eq', 'name': 'email_func', 'value': user_email}
            ]
        )
        df_aluno = dados.query_table(table_name='aluno',)
        df_aluno_turma = dados.query_table(table_name='turma_aluno',)
        df_turma = dados.query_table(table_name='turma',)

        nome_completo = df_func['nome_completo'][0]
        tipo = df_func['tipo'][0]
        msg = f'Usuário: {nome_completo} Tipo: {tipo}'
        st = [
            'ativo',
            'inativo',
            'finalizado',
            'None',
            'trancado',
        ]

        #### aluno status
        # dummy
        df_aluno['status'] =  [st[random.randrange(0, len(st))] for x in df_aluno['id']]
        agg_aluno = df_aluno.groupby(
            by=[
                pd.Grouper(key='status'),
            ],
        ).agg(
            count=pd.NamedAgg(column='status', aggfunc='count'),
        ).reset_index()


        ### aluno por ano
        atual_year = datetime.datetime.now().year
        yy = [
            atual_year,
            atual_year-1,
            atual_year-2,
            atual_year-3,
        ]
        # dummy
        df_aluno['created_at'] = [
            pd.to_datetime(f'{yy[random.randrange(0, len(yy))]}-12-31')
            for x in df_aluno['id']
        ]

        min = df_aluno['created_at'].min()
        max = df_aluno['created_at'].max()

        agg_aluno_year = df_aluno.groupby(
            by=[
                pd.Grouper(key='created_at', freq='Y'),
            ],
        ).agg(
            count=pd.NamedAgg(column='created_at', aggfunc='count'),
        ).reset_index()

        fig_aluno = go.Figure()
        fig_aluno_by_year = go.Figure()

        for year in pd.date_range(min, max, freq='Y'):
            print(year.year)

            df_aux = agg_aluno_year[agg_aluno_year['created_at'].dt.year == year.year]
            df_aux['created_at'] = df_aux['created_at'].dt.strftime('%Y')

            # cria barra
            fig_aluno_by_year.add_trace(
                go.Bar(
                    x=df_aux['created_at'],
                    y=df_aux['count'],
                    hovertemplate="<br>".join(
                        [
                            "<b> %{y}</b>",
                        ],
                    ),
                    name=f'{year.year}',
                )
            )

        for x in df_aluno['status'].unique():

            # filtro
            df_aux = agg_aluno[agg_aluno['status'] == x]

            # cria barra
            fig_aluno.add_trace(
                go.Bar(
                    x=df_aux['status'],
                    y=df_aux['count'],
                    hovertemplate="<br>".join(
                        [
                            "<b> %{y}</b>",
                        ],
                    ),
                    name=x,
                )
            )

        fig_aluno.update_layout(**config['home']['fig_aluno'])
        fig_aluno_by_year.update_layout(**config['home']['fig_aluno'])

        graph_aluno = dcc.Graph(
            figure=fig_aluno,
            # className='px-0 mx-0 shadow',
            # style=style,
            config={
                'displayModeBar': False,
            },
        )
        graph_aluno_by_year = dcc.Graph(
            figure=fig_aluno_by_year,
            # className='px-0 mx-0 shadow',
            # style=style,
            config={
                'displayModeBar': False,
            },
        )

        col1 = dbc.Col(
            class_name='col-sm-12 col-md-6 col-lg-4 ',
            children=[
                dmc.Card(
                    children=[
                        dmc.CardSection(
                            dmc.Group(
                                children=[
                                    dmc.Text('STATUS ALUNO'),
                                    dmc.ActionIcon(
                                        DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        color="gray",
                                        variant="transparent",
                                    ),
                                ],
                                position="apart",
                            ),
                            withBorder=True,
                            inheritPadding=True,
                            py="xs",
                        ),
                        dmc.CardSection(
                            children=[graph_aluno]
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    # style={"width": 350},
                )
            ]
        )
        col2 = dbc.Col(
            class_name='col-sm-12 col-md-6 col-lg-4 ',
            children=[
                dmc.Card(
                    children=[
                        dmc.CardSection(
                            dmc.Group(
                                children=[
                                    dmc.Text('ALUNOS POR ANO'),
                                    dmc.ActionIcon(
                                        DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        color="gray",
                                        variant="transparent",
                                    ),
                                ],
                                position="apart",
                            ),
                            withBorder=True,
                            inheritPadding=True,
                            py="xs",
                        ),
                        dmc.CardSection(
                            children=[graph_aluno_by_year]
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    # style={"width": 350},
                )
            ]
        )



        result = dbc.Row(
            children=[
                dbc.Row(f'Seja bem vindo!', className='justify-content-center'),
                # dbc.Row(Titulo().load(id=f'titulo-pagina-{page_name}', title_name=msg)),
                # dbc.Row(
                #     class_name='m-0 p-0',
                #     children=[
                #         col1,
                #         col2,
                #     ]
                # ),

            ],
            className='justify-content-center m-0 py-5'
        )

    except:

        result = dbc.Row(
            children=[
                'Seja bem vindo! faça login para acessar os recursos do sistema'
            ],
            className='justify-content-center m-0 p-0'
        )

    return result






