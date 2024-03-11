import datetime
import dash
import mysql.connector.errors
import pandas as pd
import sqlalchemy.exc
import json

import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo

from banco.dados import Dados
from config.config import Config

# page_name = __name__[6:].replace('.', '_')
page_name = 'EditarTurma'
dash.register_page(__name__, path=f'/{page_name}')
# require_login(__name__)

config = Config().config
dados = Dados(config['ambiente'])

content_layout = dbc.Row(
    id=f'main-container-{page_name}',
    # class_name='px-2 mx-0 shadow-lg',
    # class_name='col-lg-10',
    children=[

        # Titulo da pagina
        # Titulo().load(id='titulo-pagina', title_name='Gerenciar Usuário'),

        # PLot area 1
        # dbc.Card(
        #     class_name='py-2 my-2 mx-0 ',
        #         children=[
        #             dbc.Row(
        #                 children=[
        #                     dbc.Accordion(
        #                         children=[
        #                             dbc.AccordionItem(
        #                                 children=[
        #                                     dbc.Row(
        #                                         class_name='col-lg-12 col-sm-12',
        #                                         children=[
        #                                             # dbc.Row(
        #                                             #     children=[
        #                                             #         dbc.Row(
        #                                             #             'DATA DE REFERÊNCIA',
        #                                             #             class_name='col-lg-4 col-sm-12 '
        #                                             #         ),
        #                                             #         dbc.Row(
        #                                             #             dcc.DatePickerSingle(
        #                                             #                 id=f'inp-date-ref-{page_name}',
        #                                             #                 min_date_allowed=datetime.date(1992, 8, 12),
        #                                             #                 max_date_allowed=datetime.,
        #                                             #                 initial_visible_month=NOW,
        #                                             #                 date=NOW,
        #                                             #                 month_format='MMMM Y',
        #                                             #                 display_format='DD-MM-YYYY',
        #                                             #                 # placeholder='YY-MM-DD',
        #                                             #             ),
        #                                             #             class_name='col-lg-12 col-sm-12 '
        #                                             #         ),
        #                                             #     ]
        #                                             # ),
        #                                             dbc.Row(
        #                                                 children=[
        #                                                     dbc.Row('Tipo Usuário', class_name='col-lg-12 col-sm-12 '),
        #                                                     dbc.Row(
        #                                                         id=f'out-seletor-tipo-{page_name}',
        #                                                         children=[
        #                                                             dbc.RadioItems(
        #                                                                 id=f'inp-create-user-type-{page_name}',
        #                                                                 options={
        #                                                                     'Gerente': f'Gerente'.upper(),
        #                                                                     'Administrativo': f'Administrativo'.upper(),
        #                                                                     'Coordenador': f'Coordenador'.upper(),
        #                                                                     'Professor': f'Professor'.upper(),
        #                                                                 },
        #                                                             )
        #                                                         ],
        #                                                         class_name='col-lg-12 col-sm-12 my-2'
        #                                                     ),
        #                                                 ]
        #                                             ),
        #                                             dbc.Row(
        #                                                 children=[
        #                                                     dbc.Row('Nome Completo', class_name='col-lg-12 col-sm-12 '),
        #                                                     dbc.Input(
        #                                                         id=f'inp-create-name-{page_name}',
        #                                                         placeholder="digite aqui...",
        #                                                         size="md",
        #                                                         className="mb-3"
        #                                                     )
        #                                                 ]
        #                                             ),
        #                                             dbc.Row(
        #                                                 children=[
        #                                                     dbc.Row('Email', class_name='col-lg-12 col-sm-12 '),
        #                                                     dbc.Input(
        #                                                         id=f'inp-create-email-{page_name}',
        #                                                         placeholder="digite aqui...",
        #                                                         size="md",
        #                                                         className="mb-3"
        #                                                     ),
        #                                                 ]
        #                                             ),
        #                                             dbc.Row(
        #                                                 children=[
        #                                                     dbc.Row('Senha', class_name='col-lg-12 col-sm-12 '),
        #                                                     dbc.Input(
        #                                                         id=f'inp-create-password-{page_name}',
        #                                                         placeholder="digite aqui...",
        #                                                         type='password',
        #                                                         size="md",
        #                                                         className="mb-3"
        #                                                     ),
        #                                                 ]
        #                                             ),
        #                                             dbc.Row(
        #                                                 children=[
        #                                                     dbc.Row('Status', class_name='col-lg-12 col-sm-12 '),
        #                                                     dbc.Row(
        #                                                         id=f'out-seletor-status-{page_name}',
        #                                                         children=[
        #                                                             dbc.RadioItems(
        #                                                                 id=f'inp-create-user-status-{page_name}',
        #                                                                 options={
        #                                                                     'Ativo': f'Ativo'.upper(),
        #                                                                     'Inativo': f'Inativo'.upper(),
        #                                                                 },
        #                                                             )
        #                                                         ],
        #                                                         class_name='col-lg-12 col-sm-12 my-2'
        #                                                     ),
        #                                                 ]
        #                                             ),
        #                                             dbc.Row(
        #                                                 children=[
        #                                                     dbc.Row(
        #                                                         id='button_area',
        #                                                         class_name='d-grid d-md-block',  # gap-2
        #                                                         children=[
        #                                                             dbc.Col(
        #                                                                 # width=2,
        #                                                                 children=[
        #                                                                     dbc.Button(
        #                                                                         id=f'btn-create-user-{page_name}',
        #                                                                         children=['Salvar novo usuário'],
        #                                                                         class_name='me-2',
        #                                                                         color='primary',
        #                                                                         n_clicks=0,
        #                                                                     ),
        #                                                                 ]
        #                                                             )
        #                                                         ]
        #                                                     ),
        #                                                 ]
        #                                             ),
        #
        #
        #                                         ]
        #                                     ),
        #
        #                                 ],
        #                                 style={'background-color': '#ffffff'},
        #                                 title="Criar Funcionário"
        #                             )
        #                         ], start_collapsed=True, flush=True, style={'background-color': '#ffffff'}
        #                     ),
        #                 ], class_name=''
        #             )
        #         ]
        #     ),
        # PLot area 1
        dbc.Card(
            # color='secondary',
            class_name='py-2 my-2 mx-0 ',
            # class_name='border shadow-lg py-2 my-2 mx-0 ',
            # children=[

            # dbc.Card(
                # color='secondary',
                # class_name='border shadow-lg py-2 my-2 mx-0 ',
                children=[
                    dbc.Row(
                        children=[
                            dbc.Accordion(
                                children=[
                                    dbc.AccordionItem(
                                        children=[

                                            dbc.Row(
                                                id=f'out-edit-funcionario-{page_name}',
                                                children=[
                                                    dash_table.DataTable(
                                                        id=f'data-table-edit-user-{page_name}',
                                                    ),
                                                ]
                                            ),
                                            # dbc.Row(
                                            #     id='button_area',
                                            #     # class_name='d-grid d-md-block',  # gap-2
                                            #     class_name='pb-2 pt-2 text-center',
                                            #     children=[
                                            #         dbc.Col(
                                            #             # width=2,
                                            #             children=[
                                            #                 dbc.Button(
                                            #                     id=f'btn-buscar-usuarios-{page_name}',
                                            #                     children=['BUSCAR TURMAS'],
                                            #                     class_name='me-2',
                                            #                     color='primary',
                                            #                     n_clicks=0,
                                            #                 ),
                                            #             ]
                                            #         )
                                            #     ]
                                            # ),


                                            dbc.Tabs(
                                                children=[
                                                    dbc.Tab(
                                                        label="TURMA DETALHADA",
                                                        children=[
                                                            dbc.Row(
                                                                id=f'out-edit-func-{page_name}',
                                                                class_name='m-0 p-0',
                                                            ),
                                                            dbc.Row(
                                                                class_name='ml-0 pt-2',
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-salvar-func-edited-{page_name}',
                                                                                children=['SALVAR TURMA'],
                                                                                class_name='me-1',
                                                                                color='primary',
                                                                                n_clicks=0,
                                                                            ),
                                                                        ]
                                                                    ),

                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            html.A(
                                                                                dbc.Button(
                                                                                    id=f'btn-limpar-campos-{page_name}',
                                                                                    children=['LIMPAR CAMPOS'],
                                                                                    class_name='me-1',
                                                                                    color='light',
                                                                                    n_clicks=0,

                                                                                ),
                                                                                href=f'/{page_name}'),
                                                                        ]
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            ),
                                        ],
                                        style={'background-color': '#ffffff'},
                                        title="SELECIONAR TURMA"
                                    )
                                ], start_collapsed=False, flush=True, style={'background-color': '#ffffff'}
                            ),
                        ], class_name=''
                    )
                ]
            ),
        dbc.Alert(
            children=[
                dbc.Row(id=f'out-alert-user-{page_name}'),
                dbc.Row(id=f'out-alert-fuc-{page_name}'),
                dbc.Row(id=f'out-alert-edited-fuc-{page_name}'),
            ]
        )
    ],
        # dbc.Alert(id=f'out-alert-fuc-{page_name}'),
        # ]
        # )
#     ]
)


def layout():
    try:
        if current_user.is_authenticated and \
                dependecies.verify_active_user(session['email']) and \
                (
                        dependecies.is_admni_user(session['email']) or
                        dependecies.is_gerente_user(session['email']) or
                        dependecies.is_administrativo_user(session['email'])
                ):
                return content_layout
    except Exception as err:
        # return login_layout()
        # return redirect('/')
        return Titulo().load(id='titulo-pagina', title_name='Sem permissão')
    return Titulo().load(id='titulo-pagina', title_name='Sem permissão')


# @callback(
#     Output(component_id=f'out-alert-user-{page_name}', component_property='children'),
#
#     State(component_id=f'inp-create-user-type-{page_name}', component_property='value'),
#     State(component_id=f'inp-create-name-{page_name}', component_property='value'),
#     State(component_id=f'inp-create-email-{page_name}', component_property='value'),
#     State(component_id=f'inp-create-password-{page_name}', component_property='value'),
#     State(component_id=f'inp-create-user-status-{page_name}', component_property='value'),
#     Input(component_id=f'btn-create-user-{page_name}', component_property='n_clicks'),
#     # config_prevent_initial_callbacks=True,
# )
# def create_user(user_type, user_name, user_email, user_passdw, user_status, n_clicks):
#
#     if user_type and user_name and user_email and user_passdw:
#         config = Config().config
#         dados = Dados(config['ambiente'])
#         df_new_user = pd.DataFrame(
#             data={
#                 'email': [user_email],
#                 'password': [user_passdw],
#                 'status': [user_status],
#             }
#         )
#         df_new_func = pd.DataFrame(
#             data={
#                 'email_func': [user_email],
#
#                 'nome_completo': [user_name],
#                 'created_at': [datetime.datetime.now()],
#                 'tipo': [user_type],
#             }
#         )
#
#         try:
#             dados.insert_into_table(df=df_new_user, table_name='user')
#             dados.insert_into_table(df=df_new_func, table_name='funcionario')
#             msg = 'Usuário Criado'
#         except Exception as err:
#             msg = f'Usuário já existe: {user_email}'
#
#         return msg
#
#     if n_clicks:
#         msg = []
#
#         if not user_type:
#             msg.append('Tipo')
#
#         if not user_email:
#             msg.append('Email')
#
#         if not user_passdw:
#             msg.append('Senha')
#
#         if not user_name:
#             msg.append('Nome')
#
#         return f'Verifique se os campos estão corretos: {msg}'
#     return ''


@callback(
    Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),

    Input(component_id=f'main-container-{page_name}', component_property='children'),
    # Input(component_id=f'btn-buscar-usuarios-{page_name}', component_property='n_clicks'),
)
def buscar_turmas(btn):

    df_turma  = dados.query_table(
        table_name='turma',
        field_list=[
            {'name': 'id'},
            {'name': 'id_turma'},
            # {'name': 'semestre'},
            {'name': 'status'},
            {'name': 'nivel'},
            {'name': 'inicio'},
            {'name': 'fim'},
            {'name': 'map'},
            {'name': 'idioma'},
        ]
    )

    df_turma.sort_values(
        by=['status', 'inicio', ],
        ascending=[True, False, ],
        inplace=True
    )

    dt_user = dash_table.DataTable(
        id=f'data-table-edit-user-{page_name}',
        data=df_turma.to_dict('records'),
        columns=[{"name": i.replace('_', ' ').upper(), "id": i} for i in df_turma.columns],
        page_current=0,
        page_size=15,
        style_cell={'textAlign': 'center'},
        editable=False,
        filter_action='native',
        sort_mode="multi",
        sort_action="native",
        page_action="native",
        row_selectable="single",
        # row_selectable="multi",
        # export_columns='all',
        # export_format='xlsx',
        # export_columns='all',
        style_header={'textAlign': 'center', 'fontWeight': 'bold'},
        style_as_list_view=True,
    )
    datatable1 = dbc.Row(
        dt_user,
        class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0'
    )

    return datatable1

@callback(
    Output(component_id=f'out-edit-func-{page_name}', component_property='children'),
    Output(component_id=f'out-alert-fuc-{page_name}', component_property='children'),
    State(component_id=f'data-table-edit-user-{page_name}',  component_property='data'),
    Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
    # Input(component_id=f'btn-buscar-usuarios-{page_name}',  component_property='n_clicks'),
    # prevent_initial_callbacks=True,
    )
def editar_turma(data_drom_data_table, active_cell):

    if data_drom_data_table and active_cell:
        # camps editaveis
        # Nivel
        # Mapa
        # Professor
        # Coordenador
        # Alunos da turma

        df_turma = pd.DataFrame(data_drom_data_table)

        turma_id = df_turma['id'].iloc[active_cell[0]]
        id_dice = df_turma['id_turma'].iloc[active_cell[0]]

        df_user = dados.query_table(
            table_name='user',
            field_list=[
                {'name': 'email'},
                {'name': 'status'},
            ]
        )
        df_user['email_func'] = df_user['email']

        df_turma2  = dados.query_table(
            table_name='turma',
            # field_list=[
            #     {'name': 'email'},
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
            ]
        )

        df_turma_aluno  = dados.query_table(
            table_name='turma_aluno',
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': f'{id_dice}'},
            ]
        )
        df_turma2['id_professor'] = df_turma2['id_professor'].astype(int)
        df_turma2['id_coordenador'] = df_turma2['id_coordenador'].astype(int)

        turma_nivel  = df_turma2['nivel'][0]
        turma_map  = df_turma2['map'][0]

        df_all_aluno  = dados.query_table(
            table_name='aluno',
            # field_list=[
            #     {'name': 'email'},
            # ]
            # filter_list=[
            #     {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
            # ]
        )


        # df_prof_filted = pd.DataFrame(
        #     columns=['id', 'nome_completo']
        # )

        df_prof = dados.query_table(
            table_name='funcionario',
            field_list=[
                {'name': 'id'},
                {'name': 'email_func'},
                {'name': 'nome_completo'},
                {'name': 'tipo'},
            ],
            filter_list=[
                {'op': 'in', 'name': 'tipo','value': ['Gerente', 'Professor', 'Coordenador']},
                # {'op': 'eq', 'name': 'tipo','value': 'Professor'},
                # {'op': 'eq', 'name': 'tipo','value': 'Gerente'},
            ]
        )
        df_prof['id_professor'] = df_prof['id']
        df_prof['id_coordenador'] = df_prof['id']

        # captura horarios da turma
        df_turma_horario  = dados.query_table(
            table_name='turma_horario',
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': f'{id_dice}'},
            ]
        )
        df_turma_horario.drop(columns=['id'], inplace=True)

        # merge prof and coord
        df_turma3 = pd.merge(
            left=df_prof[['email_func', 'id_professor', 'nome_completo']],
            right=df_user,
            how='left',
            on=['email_func'],
        )
        df_turma3.rename(
            columns={
                # 'email_func': 'email_prof',
                'nome_completo': 'nome_professor',
            }, inplace=True
        )
        df_turma4 = pd.merge(
            left=df_turma3,
            right=df_prof[['email_func', 'id_coordenador', 'nome_completo']],
            how='left',
            on=['email_func'],
        )
        df_turma4.rename(
            columns={
                # 'email_func': 'email_coord',
                'nome_completo': 'nome_coordenador',
            }, inplace=True
        )

        # list_prof = json.loads(df_turma2['id_professor'][0])['email_user']
        #
        # df_prof_filted = df_prof[df_prof['email_func'].isin(
        #     list_prof
        #     # [ 'Professor', 'Coordenador']
        # )]
        # df_prof_filted = df_prof_filted[['id', 'nome_completo']]
        #
        # prof_name = df_prof_filted['nome_completo'].to_list()
        #
        # profs_cadastrados = df_prof_filted['id'].to_list()
        #
        # df_prof['cadastrado'] = df_prof['id'].apply(lambda x: 'CAD' if x in profs_cadastrados else 'NAO CAD')
        #
        # df_prof.sort_values(
        #     by=['cadastrado', 'nome_completo'],
        #     ascending=[True, True],
        #     inplace=True
        # )

        df_prof_filted = df_turma4[['id_professor', 'email_func', 'nome_professor', 'status']].copy()
        df_coord_filted = df_turma4[['id_coordenador', 'email_func', 'nome_coordenador', 'status']].copy()

        dt_prof = dbc.Select(
            id=f'data-table-edit-profs-{page_name}',
            options=[
                {
                    'label': f'{row["id_professor"]} - {row["nome_professor"]} ',
                    'value': row["id_professor"]
                }
                for i, row in df_prof_filted.iterrows()
            ],
            value='' if df_turma2['id_professor'].isna()[0] else int(df_turma2['id_professor']),
            # className='m-0 p-0',
        )

        dt_coord = dbc.Select(
            id=f'data-table-edit-coord-{page_name}',
            options=[
                {
                    'label': f'{row["id_coordenador"]} - {row["nome_coordenador"]} ',
                    'value': row["id_coordenador"]
                }
                for i, row in df_coord_filted.iterrows()
            ],
            value='' if df_turma2['id_coordenador'].isna()[0] else int(df_turma2['id_coordenador']),
            # className='m-0 p-0',
        )

            # dt_prof = dash_table.DataTable(
            #     id=f'data-table-edit-profs-{page_name}',
            #     data=df_prof_filted.to_dict('records'),
            #     columns=[
            #         {
            #             "name": i.replace('_', ' ').upper(),
            #             "id": i,
            #             # "editable": True if i == 'cadastrado' else False,
            #             # "presentation": 'dropdown' if i == 'cadastrado' else '',
            #         } for i in df_prof_filted.columns],
            #     # dropdown={
            #     #     'cadastrado': {
            #     #         'options': [
            #     #             {'label': "CAD", 'value': "CAD"},
            #     #             {'label': "NAO CAD", 'value': "NAO CAD"},
            #     #         ]
            #     #     }
            #     # },
            #     # style_cell={'textAlign': 'center'},
            #     page_size=30,
            #     filter_action='native',
            #     sort_mode="multi",
            #     sort_action="native",
            #     page_action="native",
            #     editable=False,
            #     style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            #     style_as_list_view=True,
            #
            # )
        # else:
        #     # df_prof = dados.query_table(table_name='funcionario')
        #
        #     df_prof_filted = df_prof.copy()
        #
        #     df_prof_filted = df_prof_filted[['id', 'nome_completo']]
        #
        cod = '' if df_turma2['id_professor'].isna()[0] else int(df_turma2['id_professor'])
        cod_cord = '' if df_turma2['id_coordenador'].isna()[0] else int(df_turma2['id_coordenador'])

        prof_name = df_prof[
            df_prof['id'].astype(int) == cod
        ]['nome_completo'].to_list()

        coord_name = df_prof[
            df_prof['id'].astype(int) == cod_cord
        ]['nome_completo'].to_list()


        #
        #     profs_cadastrados = df_prof_filted['id'].to_list()
        #
        #     df_prof_filted['cadastrado'] = df_prof['id'].apply(lambda x: 'CAD' if x in profs_cadastrados else 'NAO CAD')
        #
        #     df_prof_filted.sort_values(
        #         by=['cadastrado', 'nome_completo'],
        #         ascending=[True, True],
        #         inplace=True
        #     )
        #
        #     # df_prof_filted = df_prof[['id', 'nome_completo', 'cadastrado']].copy()
        #     dt_prof = dash_table.DataTable(
        #         id=f'data-table-edit-profs-{page_name}',
        #         data=df_prof_filted.to_dict('records'),
        #         columns=[
        #             {
        #                 "name": i.replace('_', ' ').upper(),
        #                 "id": i,
        #                 "editable": True if i == 'cadastrado' else False,
        #                 "presentation": 'dropdown' if i == 'cadastrado' else '',
        #             } for i in df_prof_filted.columns],
        #         dropdown={
        #             'cadastrado': {
        #                 'options': [
        #                     {'label': "CAD", 'value': "CAD"},
        #                     {'label': "NAO CAD", 'value': "NAO CAD"},
        #                 ]
        #             }
        #         },
        #         style_cell={'textAlign': 'center'},
        #         page_size=30,
        #         filter_action='native',
        #         sort_mode="multi",
        #         sort_action="native",
        #         page_action="native",
        #         editable=False,
        #         style_header={'textAlign': 'center', 'fontWeight': 'bold'},
        #         style_as_list_view=True,
        #
        #     )



        df_coord_filted = pd.DataFrame(columns=['id', 'nome_completo'])

        # coord_name = ''

        # if df_turma2['id_coordenador'].isna()[0] == False:
            # list_coord = json.loads(df_turma2['id_coordenador'][0])['email_user']
            # # list_coord = df_turma2['id_coordenador'][0].split(',')[:-1]
            # df_coord = dados.query_table(
            #     table_name='funcionario',
            #     filter_list=[
            #         {'op': 'in', 'name': 'email_func', 'value': list_coord}
            #     ]
            # )

            # df_coord_filted = df_coord[['id', 'nome_completo']]

            # coord_name = df_coord_filted['nome_completo'].to_list()



        df_hr_filted = pd.DataFrame(
            columns=['dia_semana', 'hora_inicio', 'min_inicio', 'hora_fim', 'min_fim']
        )


        if not df_turma_horario.empty :

            df_hr = dados.query_table(
                table_name='horario',
                filter_list=[
                    {'op': 'in', 'name': 'id', 'value': df_turma_horario['id_horario']}
                ]
            )

            df_hr_filted = df_hr[['dia_semana', 'hora_inicio', 'min_inicio', 'hora_fim', 'min_fim']]


        df_alunos_filted = pd.DataFrame(
            columns=['id', 'nome', 'status', 'telefone1']
        )

        if df_turma_aluno.empty == False:
            # json_alunos = json.loads(df_turma2['id_aluno'][0])

            list_alunos = df_turma_aluno['id_aluno'].to_list()
            # list_alunos = json.loads(df_turma2['id_aluno'][0])['id_aluno']
            # list_alunos = df_turma2['id_aluno'][0].split(',')[:-1]
            df_alunos = dados.query_table(
                table_name='aluno',
                filter_list=[
                    {'op': 'in', 'name': 'id', 'value': list_alunos}
                ]
            )

            df_alunos_filted = df_alunos[['id', 'nome', 'status', 'telefone1']]




        list_of_hour = []
        df_horario = dados.query_table(table_name='horario')

        if len(df_hr_filted) >=1 :
            horario_lista = [
                {
                    'label': f'{row["dia_semana"]} de {row["hora_inicio"].zfill(2)}:{row["min_inicio"].zfill(2)} até '
                             f'{row["hora_fim"].zfill(2)}:{row["min_fim"].zfill(2)}',
                    'value': row["id"]
                }
                for i, row in df_horario.iterrows()
            ]
            list_of_hour.append(
                dbc.Row(
                    children=[
                        dbc.Checklist(
                            id=f'imp-create-turma-horarios-{page_name}',
                            options=horario_lista,
                            className='m-0 p-0',
                            value=df_hr['id'].to_list()
                        )
                    ]
                )
            )

            # for x, row in df_hr_filted.iterrows():
            #     list_of_hour.append(
            #         dbc.Row(
            #             children=[
            #                 dbc.Input(
            #                     # disabled=True,
            #                     # options=[
            #                     #     {'label': id_dice, 'value': id_dice},
            #                     # ],
            #                     value=f'{row["dia_semana"]} de {row["hora_inicio"].zfill(2)}:{row["min_inicio"].zfill(2)} até'
            #                           f' {row["hora_fim"].zfill(2)}:{row["min_fim"].zfill(2)}'.upper(),
            #                     # className='m-0 p-0',
            #                 )
            #             ],
            #             className='m-0 p-0 pt-2',
            #         ),
            #     )
        else:


            horario_lista = [
                {
                    'label': f'{row["dia_semana"]} de {row["hora_inicio"].zfill(2)}:{row["min_inicio"].zfill(2)} até '
                             f'{row["hora_fim"].zfill(2)}:{row["min_fim"].zfill(2)}',
                    'value': row["id"]
                }
                for i, row in df_horario.iterrows()
            ]

            list_of_hour.append(
                dbc.Row(
                    children=[
                        dbc.Checklist(
                            id=f'imp-create-turma-horarios-{page_name}',
                            options=horario_lista,
                            className='m-0 p-0',
                            # value=df_hr['id'].to_list()
                        )
                    ]
                )
            )


        alunos_cadastrados = df_alunos_filted['id'].to_list()

        df_all_aluno['cadastrado'] = df_all_aluno['id'].apply(lambda x: 'CAD' if x in alunos_cadastrados else 'NAO CAD')

        df_all_aluno.sort_values(
            by=['cadastrado', 'nome'],
            ascending=[True, True],
            inplace=True
        )

        df_alunos_filted = df_all_aluno[['id', 'nome', 'status', 'telefone1', 'cadastrado']]

        dt_func5 = dash_table.DataTable(
            id=f'data-table-edit-func-5-{page_name}',
            data=df_alunos_filted.to_dict('records'),
            columns=[
                {
                    "name": i.replace('_', ' ').upper(),
                    "id": i,
                    "editable": True if i == 'cadastrado' else False,
                    "presentation": 'dropdown' if i == 'cadastrado' else '',
                } for i in df_alunos_filted.columns
            ],
            dropdown={
                'cadastrado': {
                    'options': [
                        {'label': "CAD", 'value': "CAD"},
                        {'label': "NAO CAD", 'value': "NAO CAD"},
                    ]
                }
            },
            style_cell={'textAlign': 'center'},
            page_size=30,
            filter_action='native',
            sort_mode="multi",
            sort_action="native",
            page_action="native",
            editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,
        )

        row1 = dbc.Row(
            children=[
                dbc.Alert(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=[f'TURMA {id_dice}'],
                                    class_name='col-lg-6 col-md-6 col-sm-12 '),
                                dbc.Col(f'PROFESSOR {prof_name}', class_name='col-lg-6 col-md-6 col-sm-12 '),
                            ],
                            class_name='p-0 m-0',
                        )
                    ],
                    # class_name = 'p-0 m-0',
                ),
            ],
            # class_name='p-0 m-0 py-2',
            # class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-2'
        )
        row_id_turma = dbc.Row(
            children=[
                dbc.Row('TURMA', className='m-0 p-0 pt-2'),
                dbc.Row(
                    children=[
                        dbc.Input(
                        # dbc.Select(
                            id=f'id-turma-dice-{page_name}',
                            disabled=True,
                            # options=[
                            #     {'label': id_dice, 'value': id_dice},
                            # ],
                            value=id_dice,
                            # className='m-0 p-0',
                         )
                    ],
                    className='m-0 p-0 pt-2',
                ),
            ],
            className='m-0 p-0',
        )
        row_professor = dbc.Row(
            children=[
                dbc.Row('PROFESSOR', className='m-0 p-0 pt-2'),
                dbc.Row(
                    children=[
                        dbc.Input(
                        # dbc.Select(
                            id=f'nome-{x}-{page_name}',
                            disabled=True,
                            # options=[
                            #     {'label': x, 'value': x},
                            # ],
                            value=x,
                            # className='m-0 p-0',
                         )
                     for x in prof_name ],
                    className='m-0 p-0 pt-2',
                ),
            ],
            className='m-0 p-0',
        )

        row_coordenador = dbc.Row(
            children=[
                dbc.Row('COORDENADOR', className='m-0 p-0 pt-2'),
                dbc.Row(
                    children=[
                        dbc.Input(
                        # dbc.Select(
                            id=f'coordenador-{x}-{page_name}',
                            disabled=True,
                            # options=[
                            #     {'label': x, 'value': x},
                            # ],
                            value=x,
                            # className='m-0 p-0',
                         )
                     for x in coord_name ],
                    className='m-0 p-0 pt-2',
                ),
            ],
            className='m-0 p-0',
        )

        row_nivel = dbc.Row(
            children=[
                dbc.Row('NIVEL', className='m-0 p-0 pt-2'),
                dbc.Row(
                    children=[
                        dbc.Select(
                            id=f'inp-create-nivel-turma-{page_name}',
                            # disabled=True,
                            options=[
                                {'label': 'Sensório Motor'.upper(), 'value': 'Sensório Motor'.upper()},
                                {'label': 'Sensório / Simbólico'.upper(), 'value': 'Sensório / Simbólico'.upper()},
                                {'label': 'Simbólico'.upper(), 'value': 'Simbólico'.upper()},
                                {'label': 'Simbólico / Intuitivo'.upper(), 'value': 'Simbólico / Intuitivo'.upper()},
                                {'label': 'Intuitivo'.upper(), 'value': 'Intuitivo'.upper()},
                                {'label': 'Operatório Iniciante I'.upper(), 'value': 'Operatório Iniciante I'.upper()},
                                {'label': 'Operatório Iniciante II'.upper(),
                                 'value': 'Operatório Iniciante II'.upper()},
                                {'label': 'Operatório Iniciante III'.upper(),
                                 'value': 'Operatório Iniciante III'.upper()},
                                {'label': 'Operatório Intermediário I'.upper(),
                                 'value': 'Operatório Intermediário I'.upper()},
                                {'label': 'Operatório Intermediário II'.upper(),
                                 'value': 'Operatório Intermediário II'.upper()},
                                {'label': 'Operatório Intermediário III'.upper(),
                                 'value': 'Operatório Intermediário III'.upper()},
                                {'label': 'Operatório Avançado I'.upper(), 'value': 'Operatório Avançado I'.upper()},
                                {'label': 'Operatório Avançado II'.upper(), 'value': 'Operatório Avançado II'.upper()},
                                {'label': 'Operatório Avançado III'.upper(),
                                 'value': 'Operatório Avançado III'.upper()},
                            ],
                            value=turma_nivel.upper()
                        )
                    ],
                    className='m-0 p-0'
                ),
            ],
            className='m-0 p-1'
        )

        row_map = dbc.Row(
            children=[
                dbc.Row('MAP', className='m-0 p-0'),
                dbc.Row(
                    children=[
                        dbc.Select(
                            id=f'inp-create-map-turma-{page_name}',
                            # disabled=True,
                            options=[
                                {'label': '1'.zfill(2), 'value': f'1'.zfill(2)},
                                {'label': '2'.zfill(2), 'value': f'2'.zfill(2)},
                                {'label': '3'.zfill(2), 'value': f'3'.zfill(2)},
                                {'label': '4'.zfill(2), 'value': f'4'.zfill(2)},
                                {'label': '5'.zfill(2), 'value': f'5'.zfill(2)},
                                {'label': '6'.zfill(2), 'value': f'6'.zfill(2)},
                                {'label': '7'.zfill(2), 'value': f'7'.zfill(2)},
                                {'label': '8'.zfill(2), 'value': f'8'.zfill(2)},
                                {'label': '9'.zfill(2), 'value': f'9'.zfill(2)},
                                {'label': '10'.zfill(2), 'value': f'10'.zfill(2)},
                                {'label': '11'.zfill(2), 'value': f'11'.zfill(2)},
                                {'label': '12'.zfill(2), 'value': f'12'.zfill(2)},
                                {'label': '13'.zfill(2), 'value': f'13'.zfill(2)},
                                {'label': '14'.zfill(2), 'value': f'14'.zfill(2)},
                                {'label': '15'.zfill(2), 'value': f'15'.zfill(2)},
                            ],
                            value=turma_map,
                        )
                    ],
                    className='m-0 p-0'
                ),
            ],
            className='m-0 p-1'
        )

        row2 = dbc.Row(
            children=[
                dbc.Accordion(
                    children=[
                        dbc.AccordionItem(
                            children=[
                                dbc.Row(
                                    dt_prof,
                                    class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0'
                                ),
                            ],
                            className='m-0 p-0',
                            style={'background-color': '#FAFAFA'},
                            title="PROFESSOR",
                        )
                    ],

                    className='m-0 p-0',
                    start_collapsed=True,
                    flush=True,
                )
             ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-2'
        )

        row_coord = dbc.Row(
            children=[
                dbc.Accordion(
                    children=[
                        dbc.AccordionItem(
                            children=[
                                dbc.Row(
                                    dt_coord,
                                    class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0'
                                ),
                            ],
                            className='m-0 p-0',
                            style={'background-color': '#FAFAFA'},
                            title="COORDENADOR",
                        )
                    ],

                    className='m-0 p-0',
                    start_collapsed=True,
                    flush=True,
                )
             ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-2'
        )

        row_aluno = dbc.Row(
            children=[
                dbc.Accordion(
                    children=[
                        dbc.AccordionItem(
                            children=[
                                dbc.Row(
                                    dt_func5,
                                    class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0'
                                ),
                            ],

                            className='m-0 p-0',
                            style={'background-color': '#FAFAFA'},
                            title="ALUNOS",
                        )
                    ],

                    className='m-0 p-0',
                    start_collapsed=True,
                    flush=True,
                )
             ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-2'
        )

        row4_content_hora = dbc.Row(
            children=[
                dbc.Accordion(
                    children=[
                        dbc.AccordionItem(
                            children=list_of_hour,
                            className='m-0 p-0',
                            # style={'background-color': '#ffffff'},
                            title="HORARIO",
                        ),
                    ],
                    className='m-0 p-0',
                    start_collapsed=True,
                    flush=True,
                    # style={'background-color': '#ffffff'}
                )
            ],
            className='m-0 p-1',
        )

        # row5 = dbc.Row(
        #     children=[
        #         dt_func5
        #     ],
        #     class_name='justify-content-center'
        #                'col-lg-12 col-md-12 col-sm-12 '
        #                'overflow-auto p-0 m-0 pt-2 py-5 '
        # )

        datatable1 = dbc.Row(
            children=[
                # data frames
                # row1,
                row_id_turma,
                row_professor,
                row_coordenador,
                row4_content_hora, # HORARIO
                row_nivel,
                row_map,
                row2,
                row_coord,

                row_aluno,
            ], class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0'
        )
    else:

        dt_func = dash_table.DataTable(id=f'data-table-edit-func-{page_name}',)

        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    return datatable1, '' if active_cell else ""


# id=f'out-alert-edited-fuc-{page_name}'

@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
    # State(component_id=f'data-table-edit-func-1-{page_name}',  component_property='data'),
    State(component_id=f'data-table-edit-func-5-{page_name}',  component_property='data'),
    State(component_id=f'data-table-edit-profs-{page_name}',  component_property='value'),
    State(component_id=f'data-table-edit-coord-{page_name}',  component_property='value'),
    # State(component_id=f'data-table-edit-func-3-{page_name}',  component_property='data'),
    State(component_id=f'inp-create-nivel-turma-{page_name}',  component_property='value'),
    State(component_id=f'inp-create-map-turma-{page_name}',  component_property='value'),
    State(component_id=f'id-turma-dice-{page_name}',  component_property='value'),
    State(component_id=f'imp-create-turma-horarios-{page_name}',  component_property='value'),

    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
    )
def salvar_turma(
        dt_aluno,
        dt_prof,
        dt_coord,
        nivel,
        map,
        id_turma_dice,
        horarios_turma,
        n_clicks
):
    # if n_clicks :
    if n_clicks or dt_aluno or dt_prof or nivel or map:

        id_turma_dice = int(id_turma_dice)
        dt_prof = int(dt_prof)
        dt_coord = int(dt_coord)
        df_aluno = pd.DataFrame(dt_aluno)


        df_turma_horario = pd.DataFrame()
        ids_horarios = None
        if horarios_turma:
            # tabela relacionamento horario
            df_turma_horario = pd.DataFrame(
                data={
                    'id_horario': horarios_turma
                    # 'id_horario': list_horarios
                }
            )
            df_turma_horario['id_turma'] = id_turma_dice



        alunos_cadastrados = df_aluno[df_aluno['cadastrado'] == 'CAD']

        df_turma = pd.DataFrame()
        # df_turma['id'] = [id]
        df_turma['id_turma'] = [id_turma_dice]
        df_turma['nivel'] = [nivel]
        df_turma['map'] = [map]

        # append alunos novos
        if len(alunos_cadastrados) >=1 :
            # list_aluno = []
            list_aluno = alunos_cadastrados['id'].to_list()
            # for x in alunos_cadastrados['id']:
            #     list_aluno.append(x)

            # df_turma['id_aluno'] = json.dumps({'id_aluno': list_aluno})

            # tabela relacionamento
            df_turma_aluno = pd.DataFrame(
                data={
                    'id_aluno' : list_aluno
                }
            )
            df_turma_aluno['id_turma'] = id_turma_dice
        else:
            df_turma['id_aluno'] = [None]

            df_turma_aluno = pd.DataFrame(
                data={
                    'id_turma': [id_turma_dice]
                }
            )

        df_turma['id_professor'] = dt_prof
        df_turma['id_coordenador'] = dt_coord



        try:

            # delete horarios
            dados.remove_from_table(
                table_name='turma_horario',
                filter_list=[
                    {'op': 'eq', 'name': 'id_turma', 'value': id_turma_dice},
                ]
            )
            if len(df_turma_horario) >= 1:
                dados.insert_into_table(df=df_turma_horario, table_name='turma_horario')

            dados.update_table(
                values=df_turma.to_dict(orient='records')[0],
                table_name='turma',
                pk_value=id_turma_dice,
                pk_name='id_turma'
            )

            # delete alunos da turma
            dados.remove_from_table(
                table_name='turma_aluno',
                filter_list=[
                    {'op': 'eq', 'name': 'id_turma', 'value': id_turma_dice},
                ]
            )
            # inserir alunos na turma
            dados.insert_into_table(table_name='turma_aluno', df=df_turma_aluno,)
            datetime.datetime.today()
            return f'TURMA ATUALIZADA: {df_turma_aluno["id_aluno"].to_list()}'

        except Exception as err:
            return str(err)

    else:
        return ""