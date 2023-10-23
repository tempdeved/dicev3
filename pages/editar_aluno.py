import datetime
import os
import base64
import PIL.Image as Image
import io
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
page_name='EditarAluno'
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
#         #                                             #                 display_format='DD-MM-YYYY',
        #                                             #                 display_format='DDYYYY-MM-DD
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
def editar_aluno(data_drom_data_table, active_cell):

    if data_drom_data_table and active_cell:

        df_user = pd.DataFrame(data_drom_data_table)
        id_aluno = df_user['id'].iloc[active_cell[0]]

        df_user = dados.query_table(
            table_name='aluno',
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': int(id_aluno)}
            ]
        )

        estados_list = config['estados']
        cidade_list = config['cidades']

        path_file = f'static/images/aluno/{df_user["foto"][0]}'
        path_no_foto = f'static/images/logo/no_foto.png'

        foto_user = path_file if os.path.isfile(path_file) else path_no_foto

        # campos = []

        # dbc.Row('created_at', class_name='pt-2 '),
        # dbc.Input(value=df_user["created_at"]),

        campos = [
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                        dbc.Row('nome'.replace('_', ' ').title(), class_name='pt-2 '),
                        dbc.Input(
                            id=f'nome-user-{page_name}',
                            value=df_user["nome"][0]
                        ),
                        # dbc.Row('nome_do_meio'.replace('_', ' ',.tittle( class_name='pt-2 '),
                        # dbc.Input(value=df_user["nome_do_meio"]),
                        # dbc.Row('ultimo_nome'.replace('_', ' ',.tittle( class_name='pt-2 '),
                        # dbc.Input(value=df_user["ultimo_nome"]),

                        dbc.Row('status'.replace('_', ' ').title(), class_name='pt-2 '),
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
                                    value=df_user["status"][0],
                                )
                            ],
                            class_name='pt-2 m-0 px-0'
                        ),

                        dbc.Row('Data Nascimento'.replace('_', ' ').title(), class_name='pt-2 '),
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
                                    # display_format='DD-MM-YYYY',
                                    display_format='YYYY-MM-DD',
                                    # placeholder='YY-MM-DD',
                                )
                            ],
                            class_name='col-lg-12 col-sm-12 mb-3 '
                        ),
                        dbc.Input(
                            value=df_user["dat_nasc"][0],
                            disabled=True
                        ),
                        ]
                    ),
                    dbc.Col(
                        children=[
                            dbc.Row('foto'.replace('_', ' ').title(), class_name='pt-2 '),
                            dbc.Row(
                                children=[
                                    html.Img(
                                        id=f'img-user-{page_name}',
                                        src=foto_user,
                                        alt=f'Aluno {df_user["nome"][0]}',
                                        className='perfil_avatar py-2 mx-auto text-center',
                                        # width=10
                                        style={'height': '300px', 'width': '300px'},
                                    ),
                                ],
                                class_name='px-0 justify-content-center'
                            ),
                            dcc.Upload(
                                id=f'upload-img-file{page_name}',
                                children=[
                                    'Arraste e Solte ou ',
                                    html.B('Selecione um Arquivo')
                                ],
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center'
                                }
                            ),


                            # dbc.Input(
                            # value=df_user["foto"][0],
                            # ),
                        ]
                    ),
                ],
            ),



            dbc.Row('Cidade Nascimento'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                dcc.Dropdown(
                    id=f'cidade-nasc-user-{page_name}',
                    className='',
                    options=cidade_list,
                    value=df_user["cidade_nascimento"][0],
                    searchable=True,
                ),
                className='pt-2 m-0 px-0'
            ),
            
            dbc.Row('endereco'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'endereco-user-{page_name}',
                      value=df_user["endereco"][0],
                      ),

            dbc.Row('numero'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'numero-user-{page_name}',
                      value=df_user["numero"][0],
                      type='number'),

            dbc.Row('complemento'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'complemento-user-{page_name}',
                      value=df_user["complemento"][0],
                      ),

            dbc.Row('bairro'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'bairro-user-{page_name}',
                      value=df_user["bairro"][0],
                      ),

            dbc.Row('cidade'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                dcc.Dropdown(
                    id=f'cidade-user-{page_name}',
                    className='',
                    options=cidade_list,
                    value=df_user["cidade"][0],
                    searchable=True,
                ),
                className='pt-2 m-0 px-0'
            ),

            dbc.Row('uf'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                dcc.Dropdown(
                    id=f'estados-user-{page_name}',
                    className='',
                    options=estados_list,
                    value=df_user["uf"][0],
                    searchable=True,
                ),
                className='pt-2 m-0 px-0'
            ),
            # dbc.Input(value=df_user["uf"][0]),

            dbc.Row('cep'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'cep-user-{page_name}',value=df_user["cep"][0]),

            dbc.Row('telefone1'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'telefone1-user-{page_name}',value=df_user["telefone1"][0]),

            dbc.Row('moradia'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'moradia-user-{page_name}',value=df_user["moradia"][0]),

            dbc.Row('inicio'.replace('_', ' ').title(), class_name='pt-2 '),
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
                        # display_format='DD-MM-YYYY',
                        display_format='YYYY-MM-DD',
                        # placeholder='YY-MM-DD',
                    )
                ],
                class_name='col-lg-12 col-sm-12 mb-3 '
            ),
            dbc.Input(value=df_user["inicio"][0], disabled=True),

            dbc.Row('n_irmaos'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(
                id=f'irmaos-user-{page_name}',
                value=df_user["n_irmaos"][0],
                type='number'
            ),

            dbc.Row('retorno'.replace('_', ' ').title(), class_name='pt-2 '),
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
                        # display_format='DD-MM-YYYY',
                        display_format='YYYY-MM-DD',
                        # placeholder='YY-MM-DD',
                    )
                ],
                class_name='col-lg-12 col-sm-12 mb-3 '
            ),
            dbc.Input(value=df_user["retorno"][0], disabled=True),

            dbc.Row('sexo'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'sexo-user-{page_name}',
                        options=[
                            {'label': 'masculino'.upper(), 'value': 'masculino'.upper()},
                            {'label': 'feminino'.upper(), 'value': 'feminino'.upper()},
                        ],
                        value=df_user["sexo"][0]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('responsavel_financeiro'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'responsavel_financeiro-user-{page_name}',value=df_user["responsavel_financeiro"][0]),

            dbc.Row('tel_responsavel_financeiro'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'tel_responsavel_financeiro-user-{page_name}',value=df_user["tel_responsavel_financeiro"][0]),

            dbc.Row('responsavel_p_filhos'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'responsavel_p_filhos-user-{page_name}',value=df_user["responsavel_p_filhos"][0]),

            dbc.Row('bairro_de_ida'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'bairro_de_ida-user-{page_name}',value=df_user["bairro_de_ida"][0]),

            dbc.Row('bairro_de_volta'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'bairro_de_volta-user-{page_name}',value=df_user["bairro_de_volta"][0]),

            dbc.Row('enviar_boleto'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'enviar-boleto-user-{page_name}',
                        options=[
                            {'label': 'sim'.upper(), 'value': 1},
                            {'label': 'não'.upper(), 'value': 0},
                        ],
                        value=df_user["enviar_boleto"][0]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('gerar_taxa'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'gerar-taxa-user-{page_name}',
                        options=[
                            {'label': 'sim'.upper(), 'value': 1},
                            {'label': 'não'.upper(), 'value': 0},
                        ],
                        value=df_user["gerar_taxa"][0]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('bolsista'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Row(
                children=[
                    dbc.Select(
                        id=f'bolsista-user-{page_name}',
                        options=[
                            {'label': 'sim'.upper(), 'value': 1},
                            {'label': 'não'.upper(), 'value': 0},
                        ],
                        value=df_user["bolsista"][0]
                    )
                ],
                class_name='pt-2 m-0 px-0'
            ),

            dbc.Row('nome_pai'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'nome_pai-user-{page_name}',value=df_user["nome_pai"][0]),

            dbc.Row('email_pai'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'email_pai-user-{page_name}',value=df_user["email_pai"][0]),

            dbc.Row('celular_pai'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'celular_pai-user-{page_name}',value=df_user["celular_pai"][0]),

            dbc.Row('tel_trabalho_pai'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'tel_trabalho_pai-user-{page_name}',value=df_user["tel_trabalho_pai"][0]),

            dbc.Row('cpf_pai'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'cpf_pai-user-{page_name}',value=df_user["cpf_pai"][0]),

            dbc.Row('profissao_pai'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'profissao_pai-user-{page_name}',value=df_user["profissao_pai"][0]),

            dbc.Row('nome_mae'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'nome_mae-user-{page_name}',value=df_user["nome_mae"][0]),

            dbc.Row('email_mae'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'email_mae-user-{page_name}',value=df_user["email_mae"][0], type='email'),

            dbc.Row('celular_mae'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'celular_mae-user-{page_name}',value=df_user["celular_mae"][0]),

            dbc.Row('tel_trabalho_mae'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'tel_trabalho_mae-user-{page_name}',value=df_user["tel_trabalho_mae"][0]),

            dbc.Row('cpf_mae'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'cpf_mae-user-{page_name}',value=df_user["cpf_mae"][0]),

            dbc.Row('profissao_mae'.replace('_', ' ').title(), class_name='pt-2 '),
            dbc.Input(id=f'profissao_mae-user-{page_name}',value=df_user["profissao_mae"][0]),

            # dbc.Row('senha'.replace('_', ' ',.tittle( class_name='pt-2 '),
            # dbc.Input(value=df_user["senha"]),
        ]

        datatable1 = dbc.Row(
            children=campos,
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0'
        )
    else:

        dt_func = dash_table.DataTable(
            id=f'data-table-edit-func-{page_name}',
        )
        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    return datatable1, ""


@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),

    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),

    State(component_id=f'data-table-edit-user-{page_name}', component_property='data'),
    State(component_id=f'data-table-edit-user-{page_name}', component_property='selected_rows'),

    State(component_id=f'nome-user-{page_name}', component_property='value'),
    State(component_id=f'status-user-{page_name}', component_property='value'),
    State(component_id=f'dat-nasc-user-{page_name}', component_property='date'),
    State(component_id=f'cidade-nasc-user-{page_name}', component_property='value'),
    State(component_id=f'endereco-user-{page_name}', component_property='value'),
    State(component_id=f'numero-user-{page_name}', component_property='value'),
    State(component_id=f'complemento-user-{page_name}', component_property='value'),
    State(component_id=f'bairro-user-{page_name}', component_property='value'),
    State(component_id=f'cidade-user-{page_name}', component_property='value'),
    State(component_id=f'estados-user-{page_name}', component_property='value'),
    State(component_id=f'cep-user-{page_name}', component_property='value'),
    State(component_id=f'telefone1-user-{page_name}', component_property='value'),
    State(component_id=f'moradia-user-{page_name}', component_property='value'),
    State(component_id=f'dat-inicio-user-{page_name}', component_property='date'),
    State(component_id=f'irmaos-user-{page_name}', component_property='value'),
    State(component_id=f'dat-retorno-user-{page_name}', component_property='date'),
    State(component_id=f'sexo-user-{page_name}', component_property='value'),
    State(component_id=f'responsavel_financeiro-user-{page_name}', component_property='value'),
    State(component_id=f'tel_responsavel_financeiro-user-{page_name}', component_property='value'),
    State(component_id=f'responsavel_p_filhos-user-{page_name}', component_property='value'),
    State(component_id=f'bairro_de_ida-user-{page_name}', component_property='value'),
    State(component_id=f'bairro_de_volta-user-{page_name}', component_property='value'),
    State(component_id=f'enviar-boleto-user-{page_name}', component_property='value'),
    State(component_id=f'gerar-taxa-user-{page_name}', component_property='value'),
    State(component_id=f'bolsista-user-{page_name}', component_property='value'),
    State(component_id=f'nome_pai-user-{page_name}', component_property='value'),
    State(component_id=f'email_pai-user-{page_name}', component_property='value'),
    State(component_id=f'celular_pai-user-{page_name}', component_property='value'),
    State(component_id=f'tel_trabalho_pai-user-{page_name}', component_property='value'),
    State(component_id=f'cpf_pai-user-{page_name}', component_property='value'),
    State(component_id=f'profissao_pai-user-{page_name}', component_property='value'),
    State(component_id=f'nome_mae-user-{page_name}', component_property='value'),
    State(component_id=f'email_mae-user-{page_name}', component_property='value'),
    State(component_id=f'celular_mae-user-{page_name}', component_property='value'),
    State(component_id=f'tel_trabalho_mae-user-{page_name}', component_property='value'),
    State(component_id=f'cpf_mae-user-{page_name}', component_property='value'),
    State(component_id=f'profissao_mae-user-{page_name}', component_property='value'),

    State(component_id=f'upload-img-file{page_name}', component_property='contents'),
    State(component_id=f'upload-img-file{page_name}', component_property='filename'),

    )
def salvar_funcionarios_editados2(
        n_clicks,
        data_drom_data_table,
        active_cell,
        nome,
        status,
        dat_nasc,
        cidade_nasc,
        endereco,
        numero,
        complemento,
        bairro,
        cidade,
        uf,
        cep,
        telefone1,
        moradia,
        dat_inicio,
        irmaos,
        dat_retorno,
        sexo,
        responsavel_financeiro,
        tel_responsavel_financeiro,
        responsavel_p_filhos,
        bairro_de_ida,
        bairro_de_volta,
        enviar_boleto,
        gerar_taxa,
        bolsista,
        nome_pai,
        email_pai,
        celular_pai,
        tel_trabalho_pai,
        cpf_pai,
        profissao_pai,
        nome_mae,
        email_mae,
        celular_mae,
        tel_trabalho_mae,
        cpf_mae,
        profissao_mae,

        img_content,
        img_name,
):
    try:
        if n_clicks:

            df_user_resume = pd.DataFrame(data_drom_data_table)
            id_aluno = int(df_user_resume['id'].iloc[active_cell[0]])

            df_user = dados.query_table(
                table_name='aluno',
                filter_list=[
                    {'op': 'eq', 'name': 'id', 'value': id_aluno}
                ]
            )

            # df_user = pd.DataFrame()
            # df_user['id'] = [id_aluno]

            if nome is not None:
                df_user['nome'] = [nome.upper()]
            if status is not None:
                df_user['status'] = [status]
            if dat_nasc is not None:
                df_user['dat_nasc'] = [dat_nasc]
            if cidade_nasc is not None:
                df_user['cidade_nascimento'] = [cidade_nasc]
            if endereco is not None:
                df_user['endereco'] = [endereco.upper()]
            if numero is not None:
                df_user['numero'] = [numero]
            if complemento is not None:
                df_user['complemento'] = [complemento.upper()]
            if bairro is not None:
                df_user['bairro'] = [bairro.upper()]
            if cidade is not None:
                df_user['cidade'] = [cidade]
            if uf is not None:
                df_user['uf'] = [uf]
            if cep is not None:
                df_user['cep'] = [cep]
            if telefone1 is not None:
                df_user['telefone1'] = [telefone1]
            if moradia is not None:
                df_user['moradia'] = [moradia.upper()]
            if dat_inicio is not None:
                df_user['inicio'] = [dat_inicio]
            if irmaos is not None:
                df_user['n_irmaos'] = [irmaos]
            if dat_retorno is not None:
                df_user['retorno'] = [dat_retorno]
            if sexo is not None:
                df_user['sexo'] = [sexo]
            if responsavel_financeiro is not None:
                df_user['responsavel_financeiro'] = [responsavel_financeiro.upper()]
            if tel_responsavel_financeiro is not None:
                df_user['tel_responsavel_financeiro'] = [tel_responsavel_financeiro]
            if responsavel_p_filhos is not None:
                df_user['responsavel_p_filhos'] = [responsavel_p_filhos.upper()]
            if bairro_de_ida is not None:
                df_user['bairro_de_ida'] = [bairro_de_ida.upper()]
            if bairro_de_volta is not None:
                df_user['bairro_de_volta'] = [bairro_de_volta.upper()]
            if enviar_boleto is not None:
                df_user['enviar_boleto'] = [int(enviar_boleto)]
            if gerar_taxa is not None:
                df_user['gerar_taxa'] = [int(gerar_taxa)]
            if bolsista is not None:
                df_user['bolsista'] = [int(bolsista)]
            if nome_pai is not None:
                df_user['nome_pai'] = [nome_pai.upper()]
            if email_pai is not None:
                df_user['email_pai'] = [email_pai]
            if celular_pai is not None:
                df_user['celular_pai'] = [celular_pai]
            if tel_trabalho_pai is not None:
                df_user['tel_trabalho_pai'] = [tel_trabalho_pai]
            if cpf_pai is not None:
                df_user['cpf_pai'] = [cpf_pai]
            if profissao_pai is not None:
                df_user['profissao_pai'] = [profissao_pai.upper()]
            if nome_mae is not None:
                df_user['nome_mae'] = [nome_mae.upper()]
            if email_mae is not None:
                df_user['email_mae'] = [email_mae]
            if celular_mae is not None:
                df_user['celular_mae'] = [celular_mae]
            if tel_trabalho_mae is not None:
                df_user['tel_trabalho_mae'] = [tel_trabalho_mae]
            if cpf_mae is not None:
                df_user['cpf_mae'] = [cpf_mae]
            if profissao_mae is not None:
                df_user['profissao_mae'] = [profissao_mae.upper()]

            try:
                df_user.dropna(inplace=True, axis=1)

                # LENDO IMAGEM
                if img_name:
                    try:
                        # convert in bytes
                        content_type, content_string = img_content.split(',')
                        decoded = base64.b64decode(content_string)

                        # read bytes
                        image = Image.open(io.BytesIO(decoded))

                        name_file = f'{id_aluno}.{image.format.lower()}'

                        image.save(fp=f'static/images/aluno/{name_file}')
                        df_user['foto'] = [f'{name_file}']

                    except Exception as err:
                        result_uploaded = html.Div(f'verifique se é o arquivo correto: {img_name}', className='text-danger')
                        return result_uploaded

                # atualizando aluno
                dados.update_table(
                    values=df_user.to_dict(orient='records')[0],
                    table_name='aluno',
                    pk_value=id_aluno,
                    pk_name='id'
                )


                return 'Aluno Salvo'

            except Exception as err:
                return str(err)

        else:
            # quando nao estiver nada selecionado
            return ''

    except Exception as err:
        print('error')
        print(err)
        return str(err)
