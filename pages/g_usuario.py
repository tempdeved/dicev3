import datetime
import dash
import pandas as pd

import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo

from banco.dados import Dados
from config.config import Config

# page_name = __name__[6:].replace('.', '_')
page_name='GerenciarUsuario'
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
                                                    # dbc.Row(
                                                    #     children=[
                                                    #         dbc.Row(
                                                    #             'DATA DE REFERÊNCIA',
                                                    #             class_name='col-lg-4 col-sm-12 '
                                                    #         ),
                                                    #         dbc.Row(
                                                    #             dcc.DatePickerSingle(
                                                    #                 id=f'inp-date-ref-{page_name}',
                                                    #                 min_date_allowed=datetime.date(1992, 8, 12),
                                                    #                 max_date_allowed=datetime.,
                                                    #                 initial_visible_month=NOW,
                                                    #                 date=NOW,
                                                    #                 month_format='MMMM Y',
                                                    #                 display_format='DD-MM-YYYY',
                                                    #                 # placeholder='YY-MM-DD',
                                                    #             ),
                                                    #             class_name='col-lg-12 col-sm-12 '
                                                    #         ),
                                                    #     ]
                                                    # ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row('Tipo Usuário', class_name='col-lg-12 col-sm-12 '),
                                                            dbc.Row(
                                                                id=f'out-seletor-tipo-{page_name}',
                                                                children=[
                                                                    dbc.RadioItems(
                                                                        id=f'inp-create-user-type-{page_name}',
                                                                        options={
                                                                            'Gerente': f'Gerente'.upper(),
                                                                            'Administrativo': f'Administrativo'.upper(),
                                                                            'Coordenador': f'Coordenador'.upper(),
                                                                            'Professor': f'Professor'.upper(),
                                                                        },
                                                                    )
                                                                ],
                                                                class_name='col-lg-12 col-sm-12 my-2'
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row('Nome Completo', class_name='col-lg-12 col-sm-12 '),
                                                            dbc.Input(
                                                                id=f'inp-create-name-{page_name}',
                                                                placeholder="digite aqui...",
                                                                size="md",
                                                                className="mb-3"
                                                            )
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row('Email', class_name='col-lg-12 col-sm-12 '),
                                                            dbc.Input(
                                                                id=f'inp-create-email-{page_name}',
                                                                placeholder="digite aqui...",
                                                                size="md",
                                                                className="mb-3"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row('Senha', class_name='col-lg-12 col-sm-12 '),
                                                            dbc.Input(
                                                                id=f'inp-create-password-{page_name}',
                                                                placeholder="digite aqui...",
                                                                type='password',
                                                                size="md",
                                                                className="mb-3"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row('Status', class_name='col-lg-12 col-sm-12 '),
                                                            dbc.Row(
                                                                id=f'out-seletor-status-{page_name}',
                                                                children=[
                                                                    dbc.RadioItems(
                                                                        id=f'inp-create-user-status-{page_name}',
                                                                        options={
                                                                            'Ativo': f'Ativo'.upper(),
                                                                            'Inativo': f'Inativo'.upper(),
                                                                        },
                                                                    )
                                                                ],
                                                                class_name='col-lg-12 col-sm-12 my-2'
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        class_name='ml-0 pt-2',
                                                        children=[
                                                            dbc.Col(
                                                                children=[
                                                                    html.A(
                                                                        dbc.Button(
                                                                            id=f'btn-limpar-campos-{page_name}',
                                                                            children=['LIMPAR CAMPOS'],
                                                                            class_name='me-1',
                                                                            color='light',
                                                                            n_clicks=0,
                                                                        ),
                                                                        href=f'/{page_name}'
                                                                    ),
                                                                ]
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    dbc.Button(
                                                                        id=f'btn-create-user-{page_name}',
                                                                        children=[
                                                                            'Salvar novo usuário'],
                                                                        class_name='me-2',
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
                                        title="Criar Funcionário"
                                    )
                                ], start_collapsed=True, flush=True, style={'background-color': '#ffffff'}
                            ),
                        ], class_name=''
                    )
                ]
            ),
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
                                            dbc.Card(
                                                class_name='d-flex justify-content-center justify-content-middle text-center py-0 my-2 mx-0 shadow',
                                                children=[
                                                    dbc.Tabs(
                                                        children=[
                                                            dbc.Tab(
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
                                                                    # children=[
                                                                        # dbc.Row(
                                                                        #     children=[
                                                                        #         dbc.Button(
                                                                        #             id=f'btn-buscar-usuarios-{page_name}',
                                                                        #             children=['Buscar Funcionários'],
                                                                        #             class_name='me-2',
                                                                        #             color='primary',
                                                                        #             n_clicks=0,
                                                                        #         ),
                                                                        #     ]
                                                                        # )

                                                                    dbc.Row(
                                                                    children=[
                                                                            dbc.Row(
                                                                            children=[
                                                                                dbc.Row(
                                                                                    id=f'button-area-{page_name}',
                                                                                    # class_name='d-grid d-md-block',  # gap-2
                                                                                    children=[
                                                                                        dbc.Col(
                                                                                            # width=2,
                                                                                            children=[
                                                                                                dbc.Button(
                                                                                                    id=f'btn-buscar-usuarios-{page_name}',
                                                                                                    children=['Buscar Funcionários'],
                                                                                                    class_name='me-2',
                                                                                                    color='primary',
                                                                                                    n_clicks=0,
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        ]
                                                                    ),
                                                                ],
                                                                label="Funcionário"
                                                            ),

                                                        ]
                                                    ),

                                                    dbc.Tabs(
                                                        children=[
                                                            dbc.Tab(
                                                                label="Campos",
                                                                children=[
                                                                    dbc.Row(id=f'out-edit-func-{page_name}'),
                                                                    dbc.Row(
                                                                        children=[
                                                                            dbc.Row(
                                                                                # id='button_area',
                                                                                # class_name='d-grid d-md-block',  # gap-2
                                                                                class_name='m-0 pt-2',
                                                                                children=[
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
                                                        ])
                                                    ,
                                                ],
                                            ),
                                        ],
                                        style={'background-color': '#ffffff'},
                                        title="Editar Funcinário"
                                    )
                                ], start_collapsed=True, flush=True, style={'background-color': '#ffffff'}
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
                (dependecies.is_admni_user(session['email']) or dependecies.is_gerente_user(session['email'])):
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

    Input(component_id=f'btn-buscar-usuarios-{page_name}', component_property='n_clicks'),
)
def capturar_funcionarios(main_contianer):

    if main_contianer >= 1:

        df_user  = dados.query_table(
            table_name='user',
            field_list=[
                {'name': 'id'},
                {'name': 'email'},
                {'name': 'status'},
            ]
        )
        df_func  = dados.query_table(
            table_name='funcionario',
            # field_list=[
            #     {'name': 'email'},
            #     {'name': 'status'},
            # ]
        )
        df_func.drop(columns=['id'], inplace=True)
        df_func.rename(columns={'email_func': 'email'}, inplace=True)

        df_merge = pd.merge(
            left=df_user,
            right=df_func,
            on=['email'],
            how='left',
        )

        df = df_merge[
            ~df_merge['tipo'].isin(
                ['Admin']
            )
        ]

        # df_func = dados.query_table(table_name='funcionario')
        #
        # df = df_func[[
        #     # 'id', 'created_at', 'status',
        #     'funcao',
        #     # 'senha',
        #     'telefone1', 'telefone2', 'dat_nasc', 'cc', 'cart_profis', 'rg',
        #     'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'uf',
        #     'cep', 'email_pessoal', 'foto'
        # ]]


        num_page = int(len(df) / 5)

        filter_columns = ['email', 'status']

        # # Criando visualização em dashDataTable dos dados formatados
        dt_user = dash_table.DataTable(
            id=f'data-table-edit-user-{page_name}',
            data=df[filter_columns].to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df[filter_columns].columns],
            page_current=0,
            page_size=10,
            style_cell={'textAlign': 'center'},
            editable=False,
            filter_action='native',
            sort_mode="multi",
            sort_action="native",
            page_action="native",
            row_selectable="single",
            # row_selectable="multi",
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,

        )
        datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

        return datatable1
    else:
        return dash_table.DataTable(
            id=f'data-table-edit-user-{page_name}',
        )

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
        email = df_user['email'].iloc[active_cell[0]]

        df_user  = dados.query_table(
            table_name='user',
            # field_list=[
            #     {'name': 'email'},
            #     {'name': 'status'},
            # ]
        filter_list=[
            # {'op': 'eq', 'name': 'tipo', 'value': 'Admin'},
            # {'op': 'eq', 'name': 'tipo', 'value': 'Gerente'},
            {'op': 'eq', 'name': 'email', 'value': email}
        ]
        )
        df_func  = dados.query_table(
            table_name='funcionario',
            # field_list=[
            #     {'name': 'email'},
            #     {'name': 'status'},
            # ]
        filter_list=[
            # {'op': 'eq', 'name': 'tipo', 'value': 'Admin'},
            # {'op': 'eq', 'name': 'tipo', 'value': 'Gerente'},
            {'op': 'eq', 'name': 'email_func', 'value': email}
        ]
        )

        df_func1 = df_func[['nome_completo', 'funcao', 'telefone1', 'telefone2', 'dat_nasc']].copy()
        df_func2 = df_func[['cc', 'cart_profis', 'rg', 'endereco', 'numero', 'complemento']].copy()
        df_func3 = df_func[['bairro', 'cidade', 'rg', 'uf', 'cep',]].copy()

        val_tipo = df_func['tipo'][0]
        val_status = df_user['status'][0]
        val_email = df_user['email'][0]

        val_senha = ''

        dt_func1 = dash_table.DataTable(
            id=f'data-table-edit-func-1-{page_name}',
            data=df_func1.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_func1.columns],
            style_cell={'textAlign': 'center'},
            editable=True,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,

        )

        dt_func2 = dash_table.DataTable(
            id=f'data-table-edit-func-2-{page_name}',
            data=df_func2.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_func2.columns],
            style_cell={'textAlign': 'center'},
            editable=True,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,

        )
        dt_func3 = dash_table.DataTable(
            id=f'data-table-edit-func-3-{page_name}',
            data=df_func3.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_func3.columns],
            style_cell={'textAlign': 'center'},
            editable=True,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,

        )

        radio_status = dbc.Row(
            children=[
                dbc.Row(
                    'Tipo Usuário',
                    class_name='col-lg-12 col-sm-12 justify-content-center ',
                    style={
                        'background-color': '#FCFCFC',
                        'font-weight': 'bold',
                    },
                ),
                dbc.Row(
                    children=[
                        dbc.RadioItems(
                            id=f'inp-edit-func-type-{page_name}',
                            options={
                                'Gerente': f'Gerente'.upper(),
                                'Administrativo': f'Administrativo'.upper(),
                                'Professor': f'Professor'.upper(),
                            },
                            value=val_tipo,
                            inline=True,
                        )
                    ],
                    class_name='col-lg-12 col-sm-12',
                ),
            ]
        ),

        radio_tipo = dbc.Row(
            children=[
                dbc.Row(
                    'Status',
                    className='col-lg-12 col-sm-12 justify-content-center ',
                    style={
                        'background-color': '#FCFCFC',
                        'font-weight': 'bold',
                    },
                ),
                dbc.Row(
                    children=[
                        dbc.RadioItems(
                            id=f'inp-edit-func-status-{page_name}',
                            options={
                                'Ativo': f'Ativo'.upper(),
                                'Inativo': f'Inativo'.upper(),
                            },
                            value=val_status,
                            inline=True
                        )
                    ],
                    class_name='col-lg-12 col-sm-12'
                ),
            ]
        ),

        email_titulo = dbc.Row(
                    id=f'title-{page_name}',
                    children=[
                        dbc.Row(
                            'Email',
                            className='col-lg-12 col-sm-12 justify-content-center ',
                            style={
                                'background-color': '#FCFCFC',
                                'font-weight': 'bold',
                            },
                        ),
                        html.H1(
                            id=f'inp-edit-func-email-{page_name}',
                            children=val_email,
                            className='py-0 px-0 mx-0',
                        )
                    ]
                )

        mudar_senha = dbc.Row(
            children=[
                dbc.Col(
                    'Senha',
                    className='col-lg-12 col-sm-12 justify-content-center ',
                    style={
                        'background-color': '#FCFCFC',
                        'font-weight': 'bold',
                    },
                ),
                dbc.Col(
                    dbc.Input(
                        id=f'inp-edit-func-password-{page_name}',
                        placeholder="altere aqui...",
                        type='password',
                        # size="md",
                        className='col-lg-6 col-sm-12 justify-content-center ',
                    ),
                )
            ]
        ),

        row1 = dbc.Row(dt_func1, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        row2 = dbc.Row(dt_func2, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        row3 = dbc.Row(dt_func3, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 pt-5 ')
        row4 = dbc.Row(radio_status, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
        row5 = dbc.Row(radio_tipo, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
        row6 = dbc.Row(email_titulo, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')
        row7 = dbc.Row(mudar_senha, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 pt-5')

        datatable1 = dbc.Row(
            children=[
                # titulo
                row6,
                # passwd
                row7,
                # radios
                row5,
                row4,

                # data frames
                row1,
                row2,
                row3,
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