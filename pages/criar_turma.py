import datetime
import dash
import mysql.connector.errors
import pandas as pd
import sqlalchemy.exc
import json
import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State, long_callback
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo

from banco.dados import Dados
from config.config import Config

# page_name = __name__[6:].replace('.', '_')
page_name = 'CriarTurma'
dash.register_page(__name__, path=f'/{page_name}')

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

                                                    dbc.Row(id=f'out-form-turma-{page_name}', className='m-0 p-0',),

                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row(
                                                                id='button_area',
                                                                # class_name='d-grid d-md-block',  # gap-2
                                                                align='end',
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        align='end',
                                                                        class_name='right',
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-create-user-{page_name}',
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
                                                                            href='/CriarTurma'),
                                                                        ]
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),


                                                ]
                                            ),

                                        ],
                                        className='m-0 p-0',
                                        style={'background-color': '#ffffff'},
                                        title="CRIAR TURMA"
                                    )
                                ],
                                className='m-0 p-0',
                                start_collapsed=False,
                                flush=True,
                                style={'background-color': '#ffffff'}
                            ),
                        ], className='m-0 p-0',
                    )
                ]
            ),
        dbc.Alert(
            children=[
                dbc.Row(id=f'out-alert-user-{page_name}'),
                dbc.Row(id=f'out-alert-user-33{page_name}'),
                dbc.Row(id=f'out-alert-fuc-{page_name}'),
                dbc.Row(id=f'out-alert-edited-fuc-{page_name}'),

                # dcc.Interval(
                #     id='inp-interval',
                #     interval=1*1000, # in milliseconds
                #     n_intervals=0
                # ),
                # dbc.Row(id=f'out-interval-{page_name}'),
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


# @callback(
#     Output(component_id=f'out-interval-{page_name}', component_property='children'),
#     Input(component_id=f'inp-interval', component_property='n_intervals'),
#     interval=10,
# )
# def interval_test(n_intervals):
#     return f'{n_intervals} - {datetime.datetime.now()}'


@callback(
    Output(component_id=f'out-form-turma-{page_name}', component_property='children'),
    Input(component_id=f'main-container-{page_name}', component_property='children'),
)
def form_create_turma(datepicker):

    df_horario = dados.query_table(table_name='horario')
    df_user = dados.query_table(table_name='user')
    df_funcionario = dados.query_table(table_name='funcionario')
    df_aluno = dados.query_table(table_name='aluno')

    df_aluno_filted = df_aluno[['id', 'nome', 'status']]
    df_aluno_filted = df_aluno_filted.fillna('').copy()

    df_funcionario.rename(columns={'email_func': 'email'}, inplace=True)

    df_users = pd.merge(
        left=df_user,
        right=df_funcionario,
        on=['email'],
        how='left',
    )

    df_professor = df_users[df_users['tipo'].isin(['Professor', 'Coordenador'])]
    df_coordenador = df_users[df_users['tipo'].isin(['Professor', 'Coordenador'])]

    horario_lista = [
        {
            'label': f'{row["dia_semana"]} de {row["hora_inicio"].zfill(2)}:{row["min_inicio"].zfill(2)} até ' 
                     f'{row["hora_fim"].zfill(2)}:{row["min_fim"].zfill(2)}',
            'value': row["id"]
        }
        for i, row in df_horario.iterrows()
    ]

    professor_lista = [
        {
            'label': f'{row["nome_completo"]} {row["status"]} ',
            'value': row["id_x"]
        }
        for i, row in df_professor.iterrows()
    ]


    row_horario = dbc.Row(
        children=[
            dbc.Accordion(
                children=[
                    dbc.AccordionItem(
                        children=[
                            dbc.Checklist(
                                id=f'imp-create-turma-horarios-{page_name}',
                                options=horario_lista,
                                className='m-0 p-0',
                            )
                        ],
                        className='m-0 p-0',
                        # style={'background-color': '#ffffff'},
                        title="SELECIONAR HORARIO",
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

    row_professor = dbc.Row(
        children=[
            dbc.Accordion(
                children=[
                    dbc.AccordionItem(
                        children=[
                            dbc.Select(
                                id=f'imp-create-turma-professor-{page_name}',
                                options=professor_lista,
                                className='m-0 p-0',
                            )
                        ],
                        className='m-0 p-0',
                        # style={'background-color': '#ffffff'},
                        title="SELECIONAR PROFESSOR",
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

    row_coordenaor = dbc.Row(
        children=[
            dbc.Accordion(
                children=[
                    dbc.AccordionItem(
                        children=[
                            dbc.Select(
                                id=f'imp-create-turma-coordenaor-{page_name}',
                                options=professor_lista,
                                className='m-0 p-0',
                            )
                        ],
                        className='m-0 p-0',
                        # style={'background-color': '#ffffff'},
                        title="SELECIONAR COORDENADOR",
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
    row_aluno = dbc.Row(
        children=[
            dbc.Accordion(
                children=[
                    dbc.AccordionItem(
                        children=[
                            dash_table.DataTable(
                                id=f'data-table-alunos-turma-{page_name}',
                                data=df_aluno_filted.to_dict('records'),
                                columns=[{"name": i.upper(), "id": i} for i in df_aluno_filted.columns],
                                page_current=0,
                                page_size=10,
                                style_cell={'textAlign': 'center'},
                                editable=False,
                                filter_action='native',
                                sort_mode="multi",
                                sort_action="native",
                                page_action="native",
                                row_selectable="multi",
                                style_header={'textAlign': 'center', 'fontWeight': 'bold'},
                                style_as_list_view=True,

                            )
                        ],
                        className='m-0 p-0',
                        # style={'background-color': '#ffffff'},
                        title="SELECIONAR ALUNOS",
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

    row_id_turma = dbc.Row(
        children=[
            dbc.Row('COD TURMA', className='m-0 p-0',),
            dbc.Row(
                children=[
                    dbc.Input(
                        id=f'inp-create-id-turma-{page_name}',
                        type="number",
                        min=0,
                        max=9999,
                        step=1,
                        className='m-0 pb-2',
                        placeholder="digite aqui o cod da turma... Ex: 2301",

                    ),
                    ],
                className='m-0 p-0',
            ),

            # dbc.Row('SEMESTRE', className='m-0 pt-2', ),
            # dbc.Row(
            #     children=[
            #         dbc.RadioItems(
            #             id=f'inp-create-semestre-{page_name}',
            #             options={
            #                 '01': f'01'.upper(),
            #                 '02': f'02'.upper(),
            #             },
            #             value=f'02' if datetime.datetime.now().month < 6 else '01',
            #             inline=True,
            #         )
            #         ],
            #     className='m-0 p-0',
            # )
            #
        ],
        className='m-0 p-1',
    )

    row_status = dbc.Row(
        children=[
            dbc.Row('STATUS', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'inp-create-status-turma-{page_name}',
                        options=[
                            {'label': 'Ativa'.upper(),'value': f'Ativa'.upper()},
                            {'label': 'Inativa'.upper(),'value': f'Inativa'.upper()},
                            {'label': 'Em espera'.upper(),'value': f'Em espera'.upper()},
                            {'label': 'Finalizadas'.upper(),'value': f'Finalizadas'.upper()},
                        ],
                    )
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )

    row_escola = dbc.Row(
        children=[
            dbc.Row('ESCOLA', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'inp-create-escola-turma-{page_name}',
                        options=[
                            {'label': 'dice - lagoa'.upper(),'value': f'dice - lagoa'.upper()},
                        ],
                        value='dice - lagoa'.upper()
                    )
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )
    row_nivel = dbc.Row(
        children=[
            dbc.Row('NIVEL', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'inp-create-nivel-turma-{page_name}',
                        options=[
                            {'label': 'Sensório Motor'.upper(), 'value': 'Sensório Motor'.upper()},
                            {'label': 'Sensório / Simbólico'.upper(), 'value': 'Sensório / Simbólico'.upper()},
                            {'label': 'Simbólico'.upper(), 'value': 'Simbólico'.upper()},
                            {'label': 'Simbólico / Intuitivo'.upper(), 'value': 'Simbólico / Intuitivo'.upper()},
                            {'label': 'Intuitivo'.upper(), 'value': 'Intuitivo'.upper()},
                            {'label': 'Operatório Iniciante I'.upper(), 'value': 'Operatório Iniciante I'.upper()},
                            {'label': 'Operatório Iniciante II'.upper(), 'value': 'Operatório Iniciante II'.upper()},
                            {'label': 'Operatório Iniciante III'.upper(), 'value': 'Operatório Iniciante III'.upper()},
                            {'label': 'Operatório Intermediário I'.upper(), 'value': 'Operatório Intermediário I'.upper()},
                            {'label': 'Operatório Intermediário II'.upper(), 'value': 'Operatório Intermediário II'.upper()},
                            {'label': 'Operatório Intermediário III'.upper(), 'value': 'Operatório Intermediário III'.upper()},
                            {'label': 'Operatório Avançado I'.upper(), 'value': 'Operatório Avançado I'.upper()},
                            {'label': 'Operatório Avançado II'.upper(), 'value': 'Operatório Avançado II'.upper()},
                            {'label': 'Operatório Avançado III'.upper(), 'value': 'Operatório Avançado III'.upper()},
                        ],
                        # value='0'.upper()
                    )
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )
    row_idioma = dbc.Row(
        children=[
            dbc.Row('IDIOMA', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'inp-create-idioma-turma-{page_name}',
                        options=[
                            {'label': 'inglês'.upper(),'value': f'inglês'.upper()},
                        ],
                        value='inglês'.upper()
                    )
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )
    row_map= dbc.Row(
        children=[
            dbc.Row('MAP', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'inp-create-map-turma-{page_name}',
                        options=[
                            {'label': '1'.upper(), 'value': f'1'.upper()},
                            {'label': '2'.upper(), 'value': f'2'.upper()},
                            {'label': '3'.upper(), 'value': f'3'.upper()},
                            {'label': '4'.upper(), 'value': f'4'.upper()},
                            {'label': '5'.upper(), 'value': f'5'.upper()},
                            {'label': '6'.upper(), 'value': f'6'.upper()},
                            {'label': '7'.upper(), 'value': f'7'.upper()},
                            {'label': '8'.upper(), 'value': f'8'.upper()},
                            {'label': '9'.upper(), 'value': f'9'.upper()},
                            {'label': '10'.upper(), 'value': f'10'.upper()},
                            {'label': '11'.upper(), 'value': f'11'.upper()},
                            {'label': '12'.upper(), 'value': f'12'.upper()},
                            {'label': '13'.upper(), 'value': f'13'.upper()},
                            {'label': '14'.upper(), 'value': f'14'.upper()},
                            {'label': '15'.upper(), 'value': f'15'.upper()},
                        ],
                    )
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )
    row_dates = dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dbc.Row('DATA INICIO', className='m-0 p-0'),
                    dbc.Row(
                        children=[
                            dcc.DatePickerSingle(
                                id=f'inp-date-inicio-turma-{page_name}',
                                min_date_allowed=datetime.date(1992, 8, 12),
                                # max_date_allowed=datetime.,
                                initial_visible_month=datetime.datetime.today(),
                                # date=datetime.datetime.today(),
                                month_format='MMMM Y',
                                display_format='DD-MM-YYYY',
                                # placeholder='YY-MM-DD',
                            )
                        ],
                        className='m-0 p-0'
                    ),
                ],
            ),
            dbc.Col(
                children=[
                    dbc.Row('DATA FIM', className='m-0 p-0'),
                    dbc.Row(
                        children=[
                            dcc.DatePickerSingle(
                                id=f'inp-date-fim-turma-{page_name}',
                                min_date_allowed=datetime.date(1992, 8, 12),
                                # max_date_allowed=datetime.,
                                initial_visible_month=datetime.datetime.today(),
                                # date=datetime.datetime.today(),
                                month_format='MMMM Y',
                                display_format='DD-MM-YYYY',
                                # placeholder='YY-MM-DD',
                            )
                        ],
                        className='m-0 p-0'
                    ),
                ],
            ),
        ],
        className='m-0 p-1'
    )
    row_descricao= dbc.Row(
        children=[
            dbc.Row('DESCRIÇÃO', className='m-0 p-0'),
            dbc.Row(
                children=[
                    dbc.Textarea(
                        id=f'inp-create-descricao-turma-{page_name}',
                        # invalid=True,
                        size="lg",
                        placeholder="Digite aqui a descrição",
                    ),
                ],
                className='m-0 p-0'
            ),
        ],
        className='m-0 p-1'
    )


    result = dbc.Row(
        children=[
            row_dates,
            row_id_turma,
            row_status,
            row_escola,
            row_nivel,
            row_idioma,
            row_map,
            row_descricao,

            row_horario,
            row_professor,
            row_coordenaor,
            row_aluno,
        ],
        className='m-0 p-0',
    )


    return result

@callback(
    Output(component_id=f'out-alert-user-{page_name}', component_property='children'),

    State(component_id=f'inp-create-id-turma-{page_name}', component_property='value'),
    # State(component_id=f'inp-create-semestre-{page_name}', component_property='value'),
    State(component_id=f'inp-create-status-turma-{page_name}', component_property='value'),
    State(component_id=f'inp-create-escola-turma-{page_name}', component_property='value'),
    State(component_id=f'inp-create-nivel-turma-{page_name}', component_property='value'),
    State(component_id=f'inp-create-idioma-turma-{page_name}', component_property='value'),
    State(component_id=f'inp-create-map-turma-{page_name}', component_property='value'),
    State(component_id=f'inp-date-inicio-turma-{page_name}', component_property='date'),
    State(component_id=f'inp-date-fim-turma-{page_name}', component_property='date'),
    State(component_id=f'inp-create-descricao-turma-{page_name}', component_property='value'),

    State(component_id=f'imp-create-turma-horarios-{page_name}', component_property='value'),
    State(component_id=f'imp-create-turma-professor-{page_name}', component_property='value'),
    State(component_id=f'imp-create-turma-coordenaor-{page_name}', component_property='value'),

    State(component_id=f'data-table-alunos-turma-{page_name}', component_property='data'),
    State(component_id=f'data-table-alunos-turma-{page_name}', component_property='selected_rows'),

    Input(component_id=f'btn-create-user-{page_name}', component_property='n_clicks'),
)
def create_turma(
        id_turma,
        # semestre_turma,
        status_turma,
        escola_turma,
        nivel_turma,
        idioma_turma,
        map,
        inicio_turma,
        fim_turma,
        descricao_turma,
        horarios_turma,
        preofessores_turma,
        coordenador_turma,
        alunos_data,
        alunos_rows,
        n_clicks,
):

    if n_clicks and id_turma and status_turma and inicio_turma and fim_turma and nivel_turma and map and preofessores_turma and coordenador_turma:

        df_alunos = pd.DataFrame(alunos_data)

        # ids_prod = None
        # if preofessores_turma:
        #     list_prof = []
        #     for x in preofessores_turma:
        #         list_prof.append(x)
        #     ids_prod = json.dumps({'email_user': list_prof})
        #
        # ids_coord = None
        # if coordenador_turma:
        #     list_coordenador = []
        #     for x in coordenador_turma:
        #         list_coordenador.append(x)
        #     ids_coord = json.dumps({'email_user': list_coordenador})

        df_turma_horario = pd.DataFrame()
        ids_horarios = None
        if horarios_turma:
            list_horarios = []
            # for x in horarios_turma:
            #     list_horarios.append(x)
            # ids_horarios = json.dumps({'id_horario': list_horarios})

            # tabela relacionamento horario
            df_turma_horario = pd.DataFrame(
                data={
                    'id_horario': list_horarios
                }
            )
            df_turma_horario['id_turma'] = id_turma

        df_new_turma= pd.DataFrame(
            data={
                'id_turma': [id_turma],
                'created_at': [datetime.datetime.now()],

                'id_professor': [preofessores_turma],
                'id_coordenador': [coordenador_turma],
                'id_hr_turma': [ids_horarios],

                # 'semestre': [semestre_turma],
                # 'numero_turma': [numero_turma], # ?????????
                'status': [status_turma],
                'escola': [escola_turma],
                'descricao': [descricao_turma],
                'nivel': [nivel_turma],
                'inicio': [inicio_turma],
                'fim': [fim_turma],
                'map': [map],
                'idioma': [idioma_turma],

            }
        )

        df_turma_aluno = pd.DataFrame()
        if alunos_rows:
            df_alunos_filted = pd.DataFrame()
            df_alunos_filted = df_alunos.iloc[alunos_rows]
            list_aluno = []
            for x in df_alunos_filted['id']:
                list_aluno.append(x)
            df_new_turma['id_aluno'] = json.dumps({'id_aluno': list_aluno})

            # tabela relacionamento
            df_turma_aluno = pd.DataFrame(
                data={
                    'id_aluno': list_aluno
                }
            )
            df_turma_aluno['id_turma'] = id_turma



        try:
            df_new_turma.dropna(axis=1, inplace=True)
            dados.insert_into_table(df=df_new_turma, table_name='turma')

            # tabelas de relacionamento
            if len(df_turma_aluno) >= 1:
                dados.insert_into_table(df=df_turma_aluno, table_name='turma_aluno')

            if len(df_turma_horario) >= 1:
                dados.insert_into_table(df=df_turma_horario, table_name='turma_horario')

            msg = f'{n_clicks} - Turma Criada'
        except Exception as err:
            msg = f'Erro: {err}'

        return msg

    if n_clicks:
        msg = []

        if not id_turma:
            msg.append('COD TURMA')
        if not status_turma:
            msg.append('STATUS')
        if not inicio_turma:
            msg.append('DATA INICIO')
        if not fim_turma:
            msg.append('DATA FIM')
        if not nivel_turma:
            msg.append('NIVEL')
        if not map:
            msg.append('MAP')
        if not preofessores_turma:
            msg.append('PROFESSOR')
        if not coordenador_turma:
            msg.append('COORDENADOR')


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
#         df_user = dados.query_table(
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
#         # df_func = dados.query_table(table_name='funcionario')
#         #
#         # df = df_func[[
#         #     # 'id', 'created_at', 'status',
#         #     'funcao',
#         #     # 'senha',
#         #     'telefone1', 'telefone2', 'dat_nasc', 'cc', 'cart_profis', 'rg',
#         #     'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'uf',
#         #     'cep', 'email_pessoal', 'foto'
#         # ]]
#
#
#         num_page = int(len(df) / 5)
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
#         val_senha = ''
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