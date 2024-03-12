import datetime
import json
import dash
import mysql.connector.errors
import pandas as pd
import sqlalchemy.exc

import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo

from banco.dados import Dados
from config.config import Config

# page_name = __name__[6:].replace('.', '_')
page_name = 'CriarALuno'
dash.register_page(__name__, path=f'/{page_name}')
# require_login(__name__)

config = Config().config
dados = Dados(config['ambiente'])

content_layout = dbc.Row(
    id=f'main-container-{page_name}',
    class_name='px-2 mx-0 shadow-lg',
    children=[

        # Titulo da pagina
        # Titulo().load(id='titulo-pagina', title_name='Gerenciar Usuário'),

        # PLot area 1
        dbc.Card(
            class_name='py-2 my-2 mx-0 ',
                children=[
                    dbc.Row(
                        children=[
                            dbc.Accordion(
                                children=[
                                    dbc.AccordionItem(
                                        children=[
                                            dbc.Row(
                                                class_name='col-lg-12 col-sm-12',
                                                children=[

                                                    dbc.Row('NOME ALUNO', class_name='col-lg-12 col-sm-12 '),
                                                    dbc.Input(
                                                        id=f'inp-create-name-{page_name}',
                                                        placeholder="digite aqui...",
                                                        size="md",
                                                        className="mb-3"
                                                    ),

                                                    dbc.Row('status'.title(), class_name='pt-2 '),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Select(
                                                                id=f'status-user-{page_name}',
                                                                options=[
                                                                    {'label': 'ativo'.upper(), 'value': 'ativo'.upper()},
                                                                    {'label': 'inativo'.upper(), 'value': 'inativo'.upper()},
                                                                    {'label': 'cancelado'.upper(), 'value': 'cancelado'.upper()},
                                                                    {'label': 'trancado'.upper(), 'value': 'trancado'.upper()},
                                                                ],
                                                                value='ativo'.upper(),
                                                            )
                                                        ],
                                                        # class_name='pt-2 m-0 px-0'
                                                    ),

                                                    dbc.Row(
                                                        class_name='pt-2 m-0 px-0',
                                                        children=[
                                                            dbc.Col(
                                                                className='col-lg-6 col-sm-12',
                                                                children=[

                                                                    dbc.Row('NOME PAI', class_name='col-lg-12 col-sm-12 '),
                                                                    dbc.Input(
                                                                        id=f'inp-name-pai-{page_name}',
                                                                        placeholder="digite aqui...",
                                                                        size="md",
                                                                        className="mb-3"
                                                                    ),

                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('EMAIL PAI', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-create-email-pai-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('CELULAR PAI', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-create-celular-pai-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('PROFISSÃO PAI', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-create-profissao-pai-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Col(
                                                                className='col-lg-6 col-sm-12',
                                                                children=[
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('NOME MÃE', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-nome-mae-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('EMAIL MÃE', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-create-email-mae-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('CELULAR MÃE', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-create-celular-mae-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),

                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row('PROFISSÃO MÃE', class_name='col-lg-12 col-sm-12 '),
                                                                            dbc.Input(
                                                                                id=f'inp-create-profissao-mae-{page_name}',
                                                                                placeholder="digite aqui...",
                                                                                size="md",
                                                                                className="mb-3"
                                                                            )
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                        className=''
                                                    ),




                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row('DATA DE INICIO', class_name='col-lg-4 col-sm-12'),
                                                            dbc.Row(
                                                                id=f'update-datepicker-{page_name}',
                                                                children=[
                                                                    dcc.DatePickerSingle(
                                                                        id=f'inp-date-inicio-aluno-{page_name}',
                                                                        min_date_allowed=datetime.date(1992, 8, 12),
                                                                        # max_date_allowed=datetime.,
                                                                        initial_visible_month=datetime.datetime.today(),
                                                                        # date=datetime.datetime.today(),
                                                                        month_format='MMMM Y',
                                                                        display_format='DD-MM-YYYY',
                                                                        # placeholder='YY-MM-DD',
                                                                    )
                                                                ],
                                                                class_name='col-lg-12 col-sm-12 mb-3 '
                                                            ),
                                                        ]
                                                    ),

                                                    dbc.Row(id=f'out-associete-turma-{page_name}',children=[], class_name='m-0 p-1'),

                                                    dbc.Row(
                                                        id=f'button-area-{page_name}',
                                                        class_name='ml-0 pt-2',  # gap-2
                                                        children=[
                                                            dbc.Col(
                                                                # width=2,
                                                                children=[
                                                                    dbc.Button(
                                                                        id=f'btn-create-user-{page_name}',
                                                                        children=['SALVAR NOVO ALUNO'],
                                                                        class_name='me-0',
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
                                        style={'background-color': '#ffffff'},
                                        title="Criar Aluno"
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
        if current_user.is_authenticated and dependecies.verify_active_user(session['email']):
                return content_layout
    except Exception as err:
        # return login_layout()
        # return redirect('/')
        return Titulo().load(id='titulo-pagina', title_name='Sem permissão')
    return Titulo().load(id='titulo-pagina', title_name='Sem permissão')


@callback(
    Output(component_id=f'update-datepicker-{page_name}', component_property='children'),
    Output(component_id=f'out-associete-turma-{page_name}', component_property='children'),
    Input(component_id=f'main-container-{page_name}', component_property='children'),
)
def update_datepicker(datepicker):

    dt_picker = dcc.DatePickerSingle(
        id=f'inp-date-inicio-aluno-{page_name}',
        min_date_allowed=datetime.date(1992, 8, 12),
        # max_date_allowed=datetime.,
        initial_visible_month=datetime.datetime.today(),
        # date=datetime.datetime.today(),
        month_format='MMMM Y',
        display_format='DD-MM-YYYY',
        # placeholder='YY-MM-DD',
    )
    print('update-date')

    df_turmas = dados.query_table(
        table_name='turma',
        # field_list=[
        #     {'name': 'email'},
        #     {'name': 'status'},
        # ]
    )
    df_turmas.sort_values(
        by=['created_at'],
        ascending=[False],
        inplace=True
    )

    row_turmas = dbc.Row(
        children=[
            dbc.Row('TURMA', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'inp-associete-turma-aluno-{page_name}',
                        options=[
                            {
                                'label': f'Turma: {row["id_turma"]} - '
                                         f'{row["status"]} '
                                         # f'semestre: {row["semestre"]} '
                                         f'inicio: {row["inicio"]} '
                                         f'fim: {row["fim"]} '
                                         f'map: {row["map"]} '
                                         f'idioma: {row["idioma"]} '
                                         f''.upper(),

                                'value': row['id']
                            }
                            for x, row in df_turmas.iterrows()
                        ],
                    )
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )


    return dt_picker, row_turmas


@callback(
    Output(component_id=f'out-alert-user-{page_name}', component_property='children'),

    State(component_id=f'inp-create-name-{page_name}', component_property='value'),
    State(component_id=f'inp-create-email-pai-{page_name}', component_property='value'),
    State(component_id=f'inp-create-celular-pai-{page_name}', component_property='value'),
    State(component_id=f'inp-create-email-mae-{page_name}', component_property='value'),
    State(component_id=f'inp-create-celular-mae-{page_name}', component_property='value'),
    State(component_id=f'inp-date-inicio-aluno-{page_name}', component_property='date'),
    State(component_id=f'inp-associete-turma-aluno-{page_name}', component_property='value'),
    State(component_id=f'status-user-{page_name}', component_property='value'),
    State(component_id=f'inp-name-pai-{page_name}', component_property='value'),
    State(component_id=f'inp-create-profissao-pai-{page_name}', component_property='value'),
    State(component_id=f'inp-nome-mae-{page_name}', component_property='value'),
    State(component_id=f'inp-create-profissao-mae-{page_name}', component_property='value'),

    Input(component_id=f'btn-create-user-{page_name}', component_property='n_clicks'),
    # config_prevent_initial_callbacks=True,
)
def create_aluno(
        user_name,
        email_pai,
        celular_pai,
        email_mae,
        celular_mae,
        data_inicio,
        turma,
        status,
        nome_pai,
        profissao_pai,
        nome_mae,
        profissao_mae,
        n_clicks,
):

    if user_name and data_inicio and status:

        created_at = datetime.datetime.now()

        df_max_aluno = dados.query_table(
            table_name='aluno',
            field_list=[
                {'name': 'id'},
            ]
        )

        max = df_max_aluno['id'].max() + 1
        print(f'ALUNO: {max}')

        df_new_aluno = pd.DataFrame(
            data={
                'id': [max],
                'created_at': [created_at],
                'nome': [user_name.upper()],
                'status': [status],
                'nome_pai': [nome_pai],
                'email_pai': [email_pai],
                'celular_pai': [celular_pai],
                'profissao_pai': [profissao_pai],
                'nome_mae': [nome_mae],
                'email_mae': [email_mae],
                'celular_mae': [celular_mae],
                'profissao_mae': [profissao_mae],
                'inicio': [data_inicio],
            }
        )

        if turma:

            df_turma = dados.query_table(
                table_name='turma',
                # field_list=[
                    # {'name': 'id_aluno'},
                # ],
                filter_list=[
                    {'op': 'eq', 'name': 'id', 'value': turma}
                ]
            )

            turma_alunos = []
            turma_alunos.append(int(max))
            # anexar novo aluno com alunos antigos
            # if df_turma['id_aluno'][0]:
            #     json_alunos = json.loads(df_turma['id_aluno'][0])
            #
            #     for x in json_alunos['id_aluno']:
            #         turma_alunos.append(x)

            # df_turma['id_aluno'] = json.dumps({'id_aluno': turma_alunos})

        df_turma_aluno = pd.DataFrame(
            data={
                'id_aluno': [max],
                'id_turma': [df_turma['id_turma'][0]],

            }
        )

        try:
            df_new_aluno.dropna(inplace=True, axis=1)
            dados.insert_into_table(df=df_new_aluno, table_name='aluno')
            dados.update_table(
                values=df_turma[['id', 'id_aluno']].to_dict(orient='records')[0],
                table_name='turma',
                pk_value=turma,
                pk_name='id'
            )


            # inserir alunos na turma Tabela ralacional
            dados.insert_into_table(table_name='turma_aluno', df=df_turma_aluno,)

            msg = f'{n_clicks} - Usuário Criado'
        except Exception as err:
            msg = f'Erro: {err}'

        return msg

    if n_clicks:
        msg = []

        if not user_name:
            msg.append('Nome')

        if not data_inicio:
            msg.append('Data de Inicio')

        return f'Verifique se os campos estão corretos: {msg}'

    return ''


# @callback(
#     Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),
#
#     Input(component_id=f'btn-buscar-usuarios-{page_name}', component_property='n_clicks'),
# )
# def capturar_funcionarios(main_contianer):
#
#     if main_contianer >= 1:
#
#         df_user  = dados.query_table(
#             table_name='user',
#             field_list=[
#                 {'name': 'id'},
#                 {'name': 'email'},
#                 {'name': 'status'},
#             ]
#         )
#         df_func  = dados.query_table(
#             table_name='funcionario',
#             # field_list=[
#             #     {'name': 'email'},
#             #     {'name': 'status'},
#             # ]
#         )
#         df_func.drop(columns=['id'], inplace=True)
#         df_func.rename(columns={'email_func': 'email'}, inplace=True)
#
#         df_merge = pd.merge(
#             left=df_user,
#             right=df_func,
#             on=['email'],
#             how='left',
#         )
#
#         df = df_merge[df_merge['tipo'].isin(['Professor', 'Gerente'])]
#
#         filter_columns = ['email', 'status']
#
#         # # Criando visualização em dashDataTable dos dados formatados
#         dt_user = dash_table.DataTable(
#             id=f'data-table-edit-user-{page_name}',
#             data=df[filter_columns].to_dict('records'),
#             columns=[{"name": i.upper(), "id": i} for i in df[filter_columns].columns],
#             page_current=0,
#             page_size=5,
#             style_cell={'textAlign': 'center'},
#             editable=False,
#             filter_action='native',
#             sort_mode="multi",
#             sort_action="native",
#             page_action="native",
#             row_selectable="single",
#             # row_selectable="multi",
#             style_header={'textAlign': 'center', 'fontWeight': 'bold'},
#
#         )
#         datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')
#
#         return datatable1
#     else:
#         return dash_table.DataTable(
#             id=f'data-table-edit-user-{page_name}',
#         )
#
# @callback(
#     Output(component_id=f'out-edit-func-{page_name}', component_property='children'),
#     Output(component_id=f'out-alert-fuc-{page_name}', component_property='children'),
#     State(component_id=f'data-table-edit-user-{page_name}',  component_property='data'),
#     Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
#     # Input(component_id=f'btn-buscar-usuarios-{page_name}',  component_property='n_clicks'),
#     # prevent_initial_callbacks=True,
#     )
# def salvar_funcionarios_editados(data_drom_data_table, active_cell):
#
#     if data_drom_data_table and active_cell:
#
#         df_user = pd.DataFrame(data_drom_data_table)
#         email = df_user['email'].iloc[active_cell[0]]
#
#         df_user  = dados.query_table(
#             table_name='user',
#             # field_list=[
#             #     {'name': 'email'},
#             #     {'name': 'status'},
#             # ]
#         filter_list=[
#             # {'op': 'eq', 'name': 'tipo', 'value': 'Admin'},
#             # {'op': 'eq', 'name': 'tipo', 'value': 'Gerente'},
#             {'op': 'eq', 'name': 'email', 'value': email}
#         ]
#         )
#         df_func  = dados.query_table(
#             table_name='funcionario',
#             # field_list=[
#             #     {'name': 'email'},
#             #     {'name': 'status'},
#             # ]
#         filter_list=[
#             # {'op': 'eq', 'name': 'tipo', 'value': 'Admin'},
#             # {'op': 'eq', 'name': 'tipo', 'value': 'Gerente'},
#             {'op': 'eq', 'name': 'email_func', 'value': email}
#         ]
#         )
#
#         df_func1 = df_func[['nome_completo', 'funcao', 'telefone1', 'telefone2', 'dat_nasc']].copy()
#         df_func2 = df_func[['cc', 'cart_profis', 'rg', 'endereco', 'numero', 'complemento']].copy()
#         df_func3 = df_func[['bairro', 'cidade', 'rg', 'uf', 'cep',]].copy()
#
#         val_tipo = df_func['tipo'][0]
#         val_status = df_user['status'][0]
#         val_email = df_user['email'][0]
#
#         dt_func1 = dash_table.DataTable(
#             id=f'data-table-edit-func-1-{page_name}',
#             data=df_func1.to_dict('records'),
#             columns=[{"name": i.upper(), "id": i} for i in df_func1.columns],
#             style_cell={'textAlign': 'center'},
#             editable=True,
#             style_header={'textAlign': 'center', 'fontWeight': 'bold'},
#
#         )
#
#         dt_func2 = dash_table.DataTable(
#             id=f'data-table-edit-func-2-{page_name}',
#             data=df_func2.to_dict('records'),
#             columns=[{"name": i.upper(), "id": i} for i in df_func2.columns],
#             style_cell={'textAlign': 'center'},
#             editable=True,
#             style_header={'textAlign': 'center', 'fontWeight': 'bold'},
#
#         )
#         dt_func3 = dash_table.DataTable(
#             id=f'data-table-edit-func-3-{page_name}',
#             data=df_func3.to_dict('records'),
#             columns=[{"name": i.upper(), "id": i} for i in df_func3.columns],
#             style_cell={'textAlign': 'center'},
#             editable=True,
#             style_header={'textAlign': 'center', 'fontWeight': 'bold'},
#
#         )
#
#         radio_status = dbc.Row(
#             children=[
#                 dbc.Row(
#                     'Tipo Usuário',
#                     class_name='col-lg-12 col-sm-12 justify-content-center ',
#                     style={
#                         'background-color': '#FCFCFC',
#                         'font-weight': 'bold',
#                     },
#                 ),
#                 dbc.Row(
#                     children=[
#                         dbc.RadioItems(
#                             id=f'inp-edit-func-type-{page_name}',
#                             options={
#                                 'Gerente': f'Gerente'.upper(),
#                                 'Administrativo': f'Administrativo'.upper(),
#                                 'Professor': f'Professor'.upper(),
#                             },
#                             value=val_tipo,
#                             inline=True,
#                         )
#                     ],
#                     class_name='col-lg-12 col-sm-12',
#                 ),
#             ]
#         ),
#
#         radio_tipo = dbc.Row(
#             children=[
#                 dbc.Row(
#                     'Status',
#                     className='col-lg-12 col-sm-12 justify-content-center ',
#                     style={
#                         'background-color': '#FCFCFC',
#                         'font-weight': 'bold',
#                     },
#                 ),
#                 dbc.Row(
#                     children=[
#                         dbc.RadioItems(
#                             id=f'inp-edit-func-status-{page_name}',
#                             options={
#                                 'Ativo': f'Ativo'.upper(),
#                                 'Inativo': f'Inativo'.upper(),
#                             },
#                             value=val_status,
#                             inline=True
#                         )
#                     ],
#                     class_name='col-lg-12 col-sm-12'
#                 ),
#             ]
#         ),
#
#         email_titulo = dbc.Row(
#                     id=f'title-{page_name}',
#                     children=[
#                         dbc.Row(
#                             'Email',
#                             className='col-lg-12 col-sm-12 justify-content-center ',
#                             style={
#                                 'background-color': '#FCFCFC',
#                                 'font-weight': 'bold',
#                             },
#                         ),
#                         html.H1(
#                             id=f'inp-edit-func-email-{page_name}',
#                             children=val_email,
#                             className='py-0 px-0 mx-0',
#                         )
#                     ]
#                 )
#
#         mudar_senha = dbc.Row(
#             children=[
#                 dbc.Col(
#                     'Senha',
#                     className='col-lg-12 col-sm-12 justify-content-center ',
#                     style={
#                         'background-color': '#FCFCFC',
#                         'font-weight': 'bold',
#                     },
#                 ),
#                 dbc.Col(
#                     dbc.Input(
#                         id=f'inp-edit-func-password-{page_name}',
#                         placeholder="altere aqui...",
#                         type='password',
#                         # size="md",
#                         className='col-lg-6 col-sm-12 justify-content-center ',
#                     ),
#                 )
#             ]
#         ),
#
#         row1 = dbc.Row(dt_func1, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
#         row2 = dbc.Row(dt_func2, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
#         row3 = dbc.Row(dt_func3, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
#         row4 = dbc.Row(radio_status, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
#         row5 = dbc.Row(radio_tipo, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
#         row6 = dbc.Row(email_titulo, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
#         row7 = dbc.Row(mudar_senha, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
#
#         datatable1 = dbc.Row(
#             children=[
#                 # titulo
#                 row6,
#                 # passwd
#                 row7,
#                 # radios
#                 row5,
#                 row4,
#
#                 # data frames
#                 row1,
#                 row2,
#                 row3,
#             ], class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0'
#         )
#     else:
#         # datatable1 = dbc.Row(children=[
#         #     dash_table.DataTable(id=f'data-table-edit-func-0-{page_name}',),
#         #     dash_table.DataTable(id=f'data-table-edit-func-1-{page_name}',),
#         #     dash_table.DataTable(id=f'data-table-edit-func-2-{page_name}',),
#         # ])
#         dt_func = dash_table.DataTable(
#             id=f'data-table-edit-func-{page_name}',
#         )
#         datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')
#
#
#     # if active_cell:
#     #     print(active_cell)
#     return datatable1, str(active_cell) if active_cell else "Click the table"
#
#
# # id=f'out-alert-edited-fuc-{page_name}'
#
# @callback(
#     Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
#     State(component_id=f'data-table-edit-func-1-{page_name}',  component_property='data'),
#     State(component_id=f'data-table-edit-func-2-{page_name}',  component_property='data'),
#     State(component_id=f'data-table-edit-func-3-{page_name}',  component_property='data'),
#     State(component_id=f'inp-edit-func-type-{page_name}',  component_property='value'),
#     State(component_id=f'inp-edit-func-status-{page_name}',  component_property='value'),
#     State(component_id=f'inp-edit-func-email-{page_name}',  component_property='children'),
#     State(component_id=f'inp-edit-func-password-{page_name}',  component_property='value'),
#     # State(component_id=f'inp-edit-func-passwd-{page_name}',  component_property='value'),
#     # Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
#     Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
#     )
# def salvar_funcionarios_editados2(dt_1, dt_2, dt_3, func_type, func_status, func_email, func_passwd, n_clicks):
#
#     if n_clicks and func_type and func_status:
#         config = Config().config
#         dados = Dados(config['ambiente'])
#
#         df1 = pd.DataFrame(dt_1)
#         df2 = pd.DataFrame(dt_2)
#         df3 = pd.DataFrame(dt_3)
#
#         df_func = pd.DataFrame()
#
#         for df in [df1, df2, df3]:
#             for column in df.columns:
#                 if len(df[column]) >=1 :
#                     df_func[column] = df[column]
#
#         df_func['tipo'] = func_type
#         df_func.dropna(axis=1, inplace=True)
#
#         df_user = pd.DataFrame()
#         df_user['status'] = [func_status]
#         if func_passwd:
#             df_user['password'] = [func_passwd]
#
#
#         try:
#             dados.update_table(values=df_user.to_dict(orient='records')[0], table_name='user', pk_value=func_email, pk_name='email')
#             dados.update_table(values=df_func.to_dict(orient='records')[0], table_name='funcionario', pk_value=func_email, pk_name='email_func')
#
#             return 'Usuário Salvo'
#         except Exception as err:
#             return str(err)
#
#
#     return str(n_clicks) if n_clicks else "Click the table"