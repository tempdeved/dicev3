import datetime
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

page_name = __name__[6:].replace('.', '_')
dash.register_page(__name__, path=f'/EditarTurma')
# require_login(__name__)


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
                                            # dbc.Card(
                                            #     class_name='d-flex justify-content-center py-0 my-2 mx-0 shadow',
                                            #     children=[
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
                                                                    dbc.Row(id=f'out-edit-func-{page_name}'),
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row(
                                                                                # id='button_area',
                                                                                # class_name='d-grid d-md-block',  # gap-2
                                                                                class_name='p-5',
                                                                                children=[
                                                                                    dbc.Col(
                                                                                        # width=2,
                                                                                        children=[
                                                                                            dbc.Button(
                                                                                                id=f'btn-salvar-func-edited-{page_name}',
                                                                                                children=[
                                                                                                    'Salvar Funcionário'],
                                                                                                # class_name='p-5',
                                                                                                color='primary',
                                                                                                n_clicks=0,
                                                                                            ),
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ]),
                                                    #     ])
                                                    # ,
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


@callback(
    Output(component_id=f'out-alert-user-{page_name}', component_property='children'),

    State(component_id=f'inp-create-user-type-{page_name}', component_property='value'),
    State(component_id=f'inp-create-name-{page_name}', component_property='value'),
    State(component_id=f'inp-create-email-{page_name}', component_property='value'),
    State(component_id=f'inp-create-password-{page_name}', component_property='value'),
    State(component_id=f'inp-create-user-status-{page_name}', component_property='value'),
    Input(component_id=f'btn-create-user-{page_name}', component_property='n_clicks'),
    # config_prevent_initial_callbacks=True,
)
def create_user(user_type, user_name, user_email, user_passdw, user_status, n_clicks):

    if user_type and user_name and user_email and user_passdw:
        config = Config().config
        dados = Dados(config['ambiente'])
        df_new_user = pd.DataFrame(
            data={
                'email': [user_email],
                'password': [user_passdw],
                'status': [user_status],
            }
        )
        df_new_func = pd.DataFrame(
            data={
                'email_func': [user_email],

                'nome_completo': [user_name],
                'created_at': [datetime.datetime.now()],
                'tipo': [user_type],
            }
        )

        try:
            dados.insert_into_table(df=df_new_user, table_name='user')
            dados.insert_into_table(df=df_new_func, table_name='funcionario')
            msg = 'Usuário Criado'
        except Exception as err:
            msg = f'Usuário já existe: {user_email}'

        return msg

    if n_clicks:
        msg = []

        if not user_type:
            msg.append('Tipo')

        if not user_email:
            msg.append('Email')

        if not user_passdw:
            msg.append('Senha')

        if not user_name:
            msg.append('Nome')

        return f'Verifique se os campos estão corretos: {msg}'
    return ''


@callback(
    Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),

    Input(component_id=f'main-container-{page_name}', component_property='children'),
    # Input(component_id=f'btn-buscar-usuarios-{page_name}', component_property='n_clicks'),
)
def buscar_turmas(btn):

    # if btn >= 1:

    config = Config().config
    dados = Dados(config['ambiente'])

    df_turma  = dados.query_table(
        table_name='turma2',
        field_list=[
            {'name': 'id'},
            {'name': 'id_turma'},
            {'name': 'semestre'},
            {'name': 'status'},
            {'name': 'nivel'},
            {'name': 'inicio'},
            {'name': 'fim'},
            {'name': 'map'},
            {'name': 'idioma'},
        ]
    )

    dt_user = dash_table.DataTable(
        id=f'data-table-edit-user-{page_name}',
        data=df_turma.to_dict('records'),
        columns=[{"name": i.upper(), "id": i} for i in df_turma.columns],
        page_current=0,
        page_size=5,
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

    )
    datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

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
        # Alunos da turma

        config = Config().config
        dados = Dados(config['ambiente'])

        df_turma = pd.DataFrame(data_drom_data_table)

        turma_id = df_turma['id'].iloc[active_cell[0]]
        id_dice = df_turma['id_turma'].iloc[active_cell[0]]

        df_turma2  = dados.query_table(
            table_name='turma2',
            # field_list=[
            #     {'name': 'email'},
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
            ]
        )


        df_prof_filted = pd.DataFrame(
            columns=['id', 'nome_completo']
        )

        if df_turma2['id_professor'].isna()[0] == False:
            list_prof = df_turma2['id_professor'][0].split(',')[:-1]
            df_prof = dados.query_table(table_name='funcionario')

            df_prof_filted = df_prof[df_prof['email_func'].isin(list_prof)]
            df_prof_filted = df_prof_filted[['id', 'nome_completo']]

            df_prof_filted2 = df_prof[df_prof['tipo'].isin(
                [ 'Professor', 'Coordenador']
            )]
            df_prof_filted2 = df_prof_filted2[['id', 'nome_completo']]



        df_coord_filted = pd.DataFrame(
            columns=['id', 'nome_completo']
        )

        if df_turma2['id_coordenador'].isna()[0] == False:
            list_coord = df_turma2['id_coordenador'][0].split(',')[:-1]
            df_coord = dados.query_table(
                table_name='funcionario',
                # field_list=[
                #     {'name': 'email'},
                # ]
            filter_list=[
                {'op': 'in', 'name': 'email_func', 'value': list_coord}
            ]
            )
            df_coord_filted = df_coord[['id', 'nome_completo']]



        df_hr_filted = pd.DataFrame(
            columns=['dia_semana', 'hora_inicio', 'min_inicio', 'hora_fim', 'min_fim']
        )

        if df_turma2['id_hr_turma'].isna()[0] == False:
            list_hr = df_turma2['id_hr_turma'][0].split(',')[:-1]
            df_hr = dados.query_table(
                table_name='horario',
                # field_list=[
                #     {'name': 'email'},
                # ]
            filter_list=[
                {'op': 'in', 'name': 'id', 'value': list_hr}
            ]
            )
            df_hr_filted = df_hr[['dia_semana', 'hora_inicio', 'min_inicio', 'hora_fim', 'min_fim']]


        df_alunos_filted = pd.DataFrame(
            columns=['id', 'nome', 'status', 'telefone1']
        )

        if df_turma2['id_aluno'].isna()[0] == False:
            list_alunos = df_turma2['id_aluno'][0].split(',')[:-1]
            df_alunos = dados.query_table(
                table_name='aluno',
                # field_list=[
                #     {'name': 'email'},
                # ]
            filter_list=[
                {'op': 'in', 'name': 'id', 'value': list_alunos}
            ]
            )
            df_alunos_filted = df_alunos[['id', 'nome', 'status', 'telefone1']]


        dt_func1 = dash_table.DataTable(
            id=f'data-table-edit-func-1-{page_name}',
            data=df_turma.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_turma.columns],
            style_cell={'textAlign': 'center'},
            editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )

        dt_func2 = dash_table.DataTable(
            id=f'data-table-edit-func-2-{page_name}',
            data=df_prof_filted.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_prof_filted.columns],
            style_cell={'textAlign': 'center'},
            editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )
        dt_func22 = dash_table.DataTable(
            id=f'data-table-edit-func-2-new-{page_name}',
            data=df_prof_filted2.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_prof_filted2.columns],
            style_cell={'textAlign': 'center'},
            editable=False,

            filter_action='native',
            page_current=0,
            page_size=1,
            row_selectable="multi",
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )
        dt_func3 = dash_table.DataTable(
            id=f'data-table-edit-func-3-{page_name}',
            data=df_coord_filted.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_coord_filted.columns],
            style_cell={'textAlign': 'center'},
            editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )
        dt_func4 = dash_table.DataTable(
            id=f'data-table-edit-func-4-{page_name}',
            data=df_hr_filted.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_hr_filted.columns],
            style_cell={'textAlign': 'center'},
            editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )
        dt_func5 = dash_table.DataTable(
            id=f'data-table-edit-func-5-{page_name}',
            data=df_alunos_filted.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_alunos_filted.columns],
            style_cell={'textAlign': 'center'},
            page_size=10,
            editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )
        #
        # radio_status = dbc.Row(
        #     children=[
        #         dbc.Row(
        #             'Tipo Usuário',
        #             class_name='col-lg-12 col-sm-12 justify-content-center ',
        #             style={
        #                 'background-color': '#FCFCFC',
        #                 'font-weight': 'bold',
        #             },
        #         ),
        #         dbc.Row(
        #             children=[
        #                 dbc.RadioItems(
        #                     id=f'inp-edit-func-type-{page_name}',
        #                     options={
        #                         'Gerente': f'Gerente'.upper(),
        #                         'Administrativo': f'Administrativo'.upper(),
        #                         'Professor': f'Professor'.upper(),
        #                     },
        #                     value=val_tipo,
        #                     inline=True,
        #                 )
        #             ],
        #             class_name='col-lg-12 col-sm-12',
        #         ),
        #     ]
        # ),
        #
        # radio_tipo = dbc.Row(
        #     children=[
        #         dbc.Row(
        #             'Status',
        #             className='col-lg-12 col-sm-12 justify-content-center ',
        #             style={
        #                 'background-color': '#FCFCFC',
        #                 'font-weight': 'bold',
        #             },
        #         ),
        #         dbc.Row(
        #             children=[
        #                 dbc.RadioItems(
        #                     id=f'inp-edit-func-status-{page_name}',
        #                     options={
        #                         'Ativo': f'Ativo'.upper(),
        #                         'Inativo': f'Inativo'.upper(),
        #                     },
        #                     value=val_status,
        #                     inline=True
        #                 )
        #             ],
        #             class_name='col-lg-12 col-sm-12'
        #         ),
        #     ]
        # ),
        #
        # email_titulo = dbc.Row(
        #             id=f'title-{page_name}',
        #             children=[
        #                 dbc.Row(
        #                     'Email',
        #                     className='col-lg-12 col-sm-12 justify-content-center ',
        #                     style={
        #                         'background-color': '#FCFCFC',
        #                         'font-weight': 'bold',
        #                     },
        #                 ),
        #                 html.H1(
        #                     id=f'inp-edit-func-email-{page_name}',
        #                     children=val_email,
        #                     className='py-0 px-0 mx-0',
        #                 )
        #             ]
        #         )
        #
        # mudar_senha = dbc.Row(
        #     children=[
        #         dbc.Col(
        #             'Senha',
        #             className='col-lg-12 col-sm-12 justify-content-center ',
        #             style={
        #                 'background-color': '#FCFCFC',
        #                 'font-weight': 'bold',
        #             },
        #         ),
        #         dbc.Col(
        #             dbc.Input(
        #                 id=f'inp-edit-func-password-{page_name}',
        #                 placeholder="altere aqui...",
        #                 type='password',
        #                 # size="md",
        #                 className='col-lg-6 col-sm-12 justify-content-center ',
        #             ),
        #         )
        #     ]
        # ),

        row1 = dbc.Row(
            children=[
                dbc.Alert(
                    children=[
                        html.Div(f'TURMA {id_dice}'),
                    ],
                ),
        ], class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-2')

        row_nivel = html.Div(
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
                            value='0'.upper()
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

        row2 = dbc.Row(
            children=[
                dbc.Accordion(
                    children=[
                        dbc.AccordionItem(
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Row('PROFESSOR ATUAL', class_name='justify-content-center'),
                                        dt_func2
                                    ],
                                    class_name='col-lg-6 col-md-12 col-sm-12 p-0 m-0 p-0 '
                                ),
                                dbc.Row(
                                    [
                                        dbc.Row('NOVO PROFESSOR', class_name='justify-content-center pt-2'),
                                        dt_func22
                                    ],
                                    class_name='col-lg-6 col-md-12 col-sm-12 p-0 m-0 p-0 '
                                )
                            ],

                            className='m-0 p-0',
                            # style={'background-color': '#ffffff'},
                            title="PROFESSOR",
                        )
                    ],

                    className='m-0 p-0',
                    start_collapsed=True,
                    flush=True,
                )
             ],
            class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 justify-content-center'
        )




        row3 = dbc.Row(
            children=[
                dbc.Row('COORDENADOR', class_name='justify-content-center'),
                dt_func3
        ], class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        row4 = dbc.Row(
            children=[
                dbc.Row('HORARIO', class_name='justify-content-center'),
                dt_func4
        ], class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')

        row5 = dbc.Row(
            children=[
                dbc.Row('ALUNOS', class_name='justify-content-center'),
                dt_func5
        ], class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')

        datatable1 = dbc.Row(
            children=[
                # data frames
                row1,
                row_nivel,
                row_map,
                row2,
                row3,
                row4,
                row5,
            ], class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0'
        )
    else:
        # datatable1 = dbc.Row(children=[
        #     dash_table.DataTable(id=f'data-table-edit-func-0-{page_name}',),
        #     dash_table.DataTable(id=f'data-table-edit-func-1-{page_name}',),
        #     dash_table.DataTable(id=f'data-table-edit-func-2-{page_name}',),
        # ])
        dt_func = dash_table.DataTable(
            id=f'data-table-edit-func-{page_name}',
        )
        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')


    # if active_cell:
    #     print(active_cell)
    return datatable1, str(active_cell) if active_cell else "Click the table"


# id=f'out-alert-edited-fuc-{page_name}'

@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
    State(component_id=f'data-table-edit-func-1-{page_name}',  component_property='data'),
    State(component_id=f'data-table-edit-func-2-{page_name}',  component_property='data'),
    State(component_id=f'data-table-edit-func-3-{page_name}',  component_property='data'),
    State(component_id=f'inp-edit-func-type-{page_name}',  component_property='value'),
    State(component_id=f'inp-edit-func-status-{page_name}',  component_property='value'),
    State(component_id=f'inp-edit-func-email-{page_name}',  component_property='children'),
    State(component_id=f'inp-edit-func-password-{page_name}',  component_property='value'),
    # State(component_id=f'inp-edit-func-passwd-{page_name}',  component_property='value'),
    # Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
    )
def salvar_funcionarios_editados2(dt_1, dt_2, dt_3, func_type, func_status, func_email, func_passwd, n_clicks):

    if n_clicks and func_type and func_status:
        config = Config().config
        dados = Dados(config['ambiente'])

        df1 = pd.DataFrame(dt_1)
        df2 = pd.DataFrame(dt_2)
        df3 = pd.DataFrame(dt_3)

        df_func = pd.DataFrame()

        for df in [df1, df2, df3]:
            for column in df.columns:
                if len(df[column]) >=1 :
                    df_func[column] = df[column]

        df_func['tipo'] = func_type
        df_func.dropna(axis=1, inplace=True)

        df_user = pd.DataFrame()
        df_user['status'] = [func_status]
        if func_passwd:
            df_user['password'] = [func_passwd]


        try:
            dados.update_table(values=df_user.to_dict(orient='records')[0], table_name='user', pk_value=func_email, pk_name='email')
            dados.update_table(values=df_func.to_dict(orient='records')[0], table_name='funcionario', pk_value=func_email, pk_name='email_func')

            return 'Usuário Salvo'
        except Exception as err:
            return str(err)


    return str(n_clicks) if n_clicks else "Click the table"