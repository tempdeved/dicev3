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

# page_name = __name__[6:].replace('.', '_')
page_name='/EditarAluno'
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
        #                                                             dbc.Row(
        #                                                                 children=[
        #                                                                     dbc.Col(
        #                                                                         # width=2,
        #                                                                         children=[
        #                                                                             html.A(
        #                                                                                 dbc.Button(
        #                                                                                     id=f'btn-limpar-campos-{page_name}',
        #                                                                                     children=['LIMPAR CAMPOS'],
        #                                                                                     class_name='me-1',
        #                                                                                     color='light',
        #                                                                                     n_clicks=0,
        #
        #                                                                                 ),
        #                                                                                 href=page_name),
        #                                                                         ]
        #                                                                     ),
        #                                                                     dbc.Col(
        #                                                                         # width=2,
        #                                                                         children=[
        #                                                                             dbc.Button(
        #                                                                                 id=f'btn-create-user-{page_name}',
        #                                                                                 children=[
        #                                                                                     'Salvar novo usuário'],
        #                                                                                 class_name='me-2',
        #                                                                                 color='primary',
        #                                                                                 n_clicks=0,
        #                                                                             ),
        #                                                                         ]
        #                                                                     )
        #                                                                 ],
        #                                                             ),
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
                                            #     id=f'button-area-{page_name}',
                                            #     # class_name='d-grid d-md-block',  # gap-2
                                            #     children=[
                                            #         dbc.Col(
                                            #             # width=2,
                                            #             children=[
                                            #                 dbc.Button(
                                            #                     id=f'btn-buscar-usuarios-{page_name}',
                                            #                     children=[
                                            #                         'Buscar Funcionários'],
                                            #                     class_name='me-2',
                                            #                     color='primary',
                                            #                     n_clicks=0,
                                            #                 ),
                                            #             ]
                                            #         )
                                            #     ]
                                            # ),
                                            dbc.Row(id=f'out-edit-func-{page_name}'),
                                            dbc.Row(
                                                children=[
                                                    dbc.Row(
                                                        # id='button_area',
                                                        # class_name='d-grid d-md-block',  # gap-2
                                                        class_name='pt-2',
                                                        children=[
                                                            dbc.Col(
                                                                # width=2,
                                                                children=[
                                                                    dbc.Button(
                                                                        id=f'btn-salvar-func-edited-{page_name}',
                                                                        children=['Salvar Aluno'],
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
                                        ],
                                        style={'background-color': '#ffffff'},
                                        title="Editar ALuno"
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
                        dependecies.is_administrativo_user(session['email']) or
                        dependecies.is_gerente_user(session['email'])
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
)
def capturar_alunos(main_contianer):


    df_aluno  = dados.query_table(
        table_name='aluno',
        # field_list=[
        #     {'name': 'email'},
        #     {'name': 'status'},
        # ]
    )

    df_aluno.sort_values(
        by=['created_at', 'status', 'nome'],
        ascending=[False, True, True],
        inplace=True
    )

    filter_columns = ['id', 'nome', 'status', 'dat_nasc', 'telefone1', 'inicio', 'tel_responsavel_financeiro']

    colulmn_type = {
        'id':'numeric',
        'nome':'text',
        'status':'text',
        'dat_nasc':'',
        'telefone1':'',
        'inicio':'',
        'tel_responsavel_financeiro':'',
    }

    # Criando visualização em dashDataTable dos dados formatados
    dt_user = dash_table.DataTable(
        id=f'data-table-edit-user-{page_name}',
        data=df_aluno[filter_columns].to_dict('records'),
        columns=[
            {
                "name": i.replace('_', ' ').upper(),
                "id": i,
                'type': colulmn_type[i]
             } for i in df_aluno[filter_columns]   .columns],
        page_current=0,
        page_size=5,
        style_cell={'textAlign': 'center'},
        editable=False,
        filter_action='native',
        sort_mode="multi",
        sort_action="native",
        page_action="native",
        row_selectable="single",
        # export_columns='all',
        # export_format='xlsx',
        # row_selectable="multi",
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
def salvar_funcionarios_editados(data_drom_data_table, active_cell):

    if data_drom_data_table and active_cell:

        df_user = pd.DataFrame(data_drom_data_table)
        id_aluno = df_user['id'].iloc[active_cell[0]]

        df_user = dados.query_table(
            table_name='aluno',
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': int(id_aluno)}
            ]
        )
        cidade_list = ['rj', 'sp']
        campos = [

            dbc.Row('foto', class_name='pt-2 '),
            dbc.Input(value=df_user["foto"]),

            # dbc.Row('created_at', class_name='pt-2 '),
            # dbc.Input(value=df_user["created_at"]),
            dbc.Row('nome', class_name='pt-2 '),
            dbc.Input(value=df_user["nome"]),
            # dbc.Row('nome_do_meio', class_name='pt-2 '),
            # dbc.Input(value=df_user["nome_do_meio"]),
            # dbc.Row('ultimo_nome', class_name='pt-2 '),
            # dbc.Input(value=df_user["ultimo_nome"]),

            dbc.Row('status', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'status-user-{page_name}',
                        options=[
                            {'label': 'ativo'.upper(), 'value': 'ativo'.upper()},
                            {'label': 'inativo'.upper(), 'value': 'inativo'.upper()},
                            {'label': 'jubilado'.upper(), 'value': 'jubilado'.upper()},
                            {'label': 'encerrado'.upper(), 'value': 'encerrado'.upper()},
                        ],
                        value=df_user["status"]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('Data Nascimento', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dcc.DatePickerSingle(
                        id=f'dat-nasc-user-{page_name}',
                        min_date_allowed=datetime.date(1900, 8, 12),
                        # max_date_allowed=datetime.,
                        initial_visible_month=df_user["dat_nasc"][0],
                        # initial_visible_month=datetime.datetime.today(),
                        # date=datetime.datetime.today(),
                        month_format='MMMM Y',
                        display_format='DD-MM-YYYY',
                        # placeholder='YY-MM-DD',
                    )
                ],
                class_name='col-lg-12 col-sm-12 mb-3 '
            ),
            dbc.Input(value=df_user["dat_nasc"], disabled=True),


            dbc.Row('Cidade Nascimento', class_name='pt-2 '),
            dbc.Row(
                dcc.Dropdown(
                    id=f'cidade-nasc-user-{page_name}',
                    className='',
                    options=cidade_list,
                    value='rj'.upper(),
                    searchable=True,
                ),
                className='pt-2 m-0 px-0'
            ),
            
            dbc.Row('endereco', class_name='pt-2 '),
            dbc.Input(value=df_user["endereco"]),

            dbc.Row('numero', class_name='pt-2 '),
            dbc.Input(value=df_user["numero"], type='number'),

            dbc.Row('complemento', class_name='pt-2 '),
            dbc.Input(value=df_user["complemento"]),

            dbc.Row('bairro', class_name='pt-2 '),
            dbc.Input(value=df_user["bairro"]),

            dbc.Row('cidade', class_name='pt-2 '),
            dbc.Row(
                dcc.Dropdown(
                    id=f'cidade-user-{page_name}',
                    className='',
                    options=cidade_list,
                    value='rj'.upper(),
                    searchable=True,
                ),
                className='pt-2 m-0 px-0'
            ),

            dbc.Row('uf', class_name='pt-2 '),
            dbc.Input(value=df_user["uf"]),

            dbc.Row('cep', class_name='pt-2 '),
            dbc.Input(value=df_user["cep"]),

            dbc.Row('telefone1', class_name='pt-2 '),
            dbc.Input(value=df_user["telefone1"]),

            dbc.Row('moradia', class_name='pt-2 '),
            dbc.Input(value=df_user["moradia"]),

            dbc.Row('inicio', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dcc.DatePickerSingle(
                        id=f'dat-inicio-user-{page_name}',
                        min_date_allowed=datetime.date(1900, 8, 12),
                        # max_date_allowed=datetime.,
                        initial_visible_month=df_user["inicio"][0],
                        # initial_visible_month=datetime.datetime.today(),
                        # date=datetime.datetime.today(),
                        month_format='MMMM Y',
                        display_format='DD-MM-YYYY',
                        # placeholder='YY-MM-DD',
                    )
                ],
                class_name='col-lg-12 col-sm-12 mb-3 '
            ),
            dbc.Input(value=df_user["inicio"], disabled=True),

            dbc.Row('n_irmaos', class_name='pt-2 '),
            dbc.Input(value=df_user["n_irmaos"], type='number'),

            dbc.Row('retorno', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dcc.DatePickerSingle(
                        id=f'dat-retorno-user-{page_name}',
                        min_date_allowed=datetime.date(1900, 8, 12),
                        # max_date_allowed=datetime.,
                        initial_visible_month=df_user["retorno"][0],
                        # initial_visible_month=datetime.datetime.today(),
                        # date=datetime.datetime.today(),
                        month_format='MMMM Y',
                        display_format='DD-MM-YYYY',
                        # placeholder='YY-MM-DD',
                    )
                ],
                class_name='col-lg-12 col-sm-12 mb-3 '
            ),
            dbc.Input(value=df_user["retorno"], disabled=True),

            dbc.Row('sexo', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'sexo-user-{page_name}',
                        options=[
                            {'label': 'masculino'.upper(), 'value': 'masculino'.upper()},
                            {'label': 'feminino'.upper(), 'value': 'feminino'.upper()},
                        ],
                        value=df_user["sexo"]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('responsavel_financeiro', class_name='pt-2 '),
            dbc.Input(value=df_user["responsavel_financeiro"]),

            dbc.Row('tel_responsavel_financeiro', class_name='pt-2 '),
            dbc.Input(value=df_user["tel_responsavel_financeiro"]),

            dbc.Row('responsavel_p_filhos', class_name='pt-2 '),
            dbc.Input(value=df_user["responsavel_p_filhos"]),

            dbc.Row('bairro_de_ida', class_name='pt-2 '),
            dbc.Input(value=df_user["bairro_de_ida"]),

            dbc.Row('bairro_de_volta', class_name='pt-2 '),
            dbc.Input(value=df_user["bairro_de_volta"]),

            dbc.Row('enviar_boleto', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'enviar-boleto-user-{page_name}',
                        options=[
                            {'label': 'sim'.upper(), 'value': 1},
                            {'label': 'não'.upper(), 'value': 0},
                        ],
                        value=df_user["enviar_boleto"]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('gerar_taxa', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'gerar-taxa-user-{page_name}',
                        options=[
                            {'label': 'sim'.upper(), 'value': 1},
                            {'label': 'não'.upper(), 'value': 0},
                        ],
                        value=df_user["gerar_taxa"]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('bolsista', class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'bolsista-user-{page_name}',
                        options=[
                            {'label': 'sim'.upper(), 'value': 1},
                            {'label': 'não'.upper(), 'value': 0},
                        ],
                        value=df_user["bolsista"]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('nome_pai', class_name='pt-2 '),
            dbc.Input(value=df_user["nome_pai"]),

            dbc.Row('email_pai', class_name='pt-2 '),
            dbc.Input(value=df_user["email_pai"]),

            dbc.Row('celular_pai', class_name='pt-2 '),
            dbc.Input(value=df_user["celular_pai"]),

            dbc.Row('tel_trabalho_pai', class_name='pt-2 '),
            dbc.Input(value=df_user["tel_trabalho_pai"]),

            dbc.Row('cpf_pai', class_name='pt-2 '),
            dbc.Input(value=df_user["cpf_pai"]),

            dbc.Row('profissao_pai', class_name='pt-2 '),
            dbc.Input(value=df_user["profissao_pai"]),

            dbc.Row('nome_mae', class_name='pt-2 '),
            dbc.Input(value=df_user["nome_mae"]),

            dbc.Row('email_mae', class_name='pt-2 '),
            dbc.Input(value=df_user["email_mae"], type='email'),

            dbc.Row('celular_mae', class_name='pt-2 '),
            dbc.Input(value=df_user["celular_mae"]),

            dbc.Row('tel_trabalho_mae', class_name='pt-2 '),
            dbc.Input(value=df_user["tel_trabalho_mae"]),

            dbc.Row('cpf_mae', class_name='pt-2 '),
            dbc.Input(value=df_user["cpf_mae"]),

            dbc.Row('profissao_mae', class_name='pt-2 '),
            dbc.Input(value=df_user["profissao_mae"]),

            # dbc.Row('senha', class_name='pt-2 '),
            # dbc.Input(value=df_user["senha"]),
        ]

        # txt_columns = [
        #     'nome',
        # ]
        #
        #
        # df_func1 = df_user[['nome', 'status', 'telefone1', 'telefone2', 'dat_nasc']].copy()
        # df_func2 = df_user[['cc', 'cart_profis', 'rg', 'endereco', 'numero', 'complemento']].copy()
        # df_func3 = df_user[['bairro', 'cidade', 'rg', 'uf', 'cep',]].copy()
        #
        # val_tipo = df_func['tipo'][0]
        # val_status = df_user['status'][0]
        # val_email = df_user['email'][0]

        val_senha = ''

        # dt_func1 = dash_table.DataTable(
        #     id=f'data-table-edit-func-1-{page_name}',
        #     data=df_func1.to_dict('records'),
        #     columns=[{"name": i.upper(), "id": i} for i in df_func1.columns],
        #     style_cell={'textAlign': 'center'},
        #     editable=True,
        #     style_header={'textAlign': 'center', 'fontWeight': 'bold'},
        #
        # )
        #
        # dt_func2 = dash_table.DataTable(
        #     id=f'data-table-edit-func-2-{page_name}',
        #     data=df_func2.to_dict('records'),
        #     columns=[{"name": i.upper(), "id": i} for i in df_func2.columns],
        #     style_cell={'textAlign': 'center'},
        #     editable=True,
        #     style_header={'textAlign': 'center', 'fontWeight': 'bold'},
        #
        # )
        # dt_func3 = dash_table.DataTable(
        #     id=f'data-table-edit-func-3-{page_name}',
        #     data=df_func3.to_dict('records'),
        #     columns=[{"name": i.upper(), "id": i} for i in df_func3.columns],
        #     style_cell={'textAlign': 'center'},
        #     editable=True,
        #     style_header={'textAlign': 'center', 'fontWeight': 'bold'},
        #
        # )
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
        #
        # row1 = dbc.Row(dt_func1, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        # row2 = dbc.Row(dt_func2, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        # row3 = dbc.Row(dt_func3, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        # row4 = dbc.Row(radio_status, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
        # row5 = dbc.Row(radio_tipo, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
        # row6 = dbc.Row(email_titulo, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
        # row7 = dbc.Row(mudar_senha, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')

        datatable1 = dbc.Row(
            children=campos,
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0'
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
    return datatable1, str(active_cell) if active_cell else ""


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