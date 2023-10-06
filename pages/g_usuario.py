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

page_name = __name__[6:].replace('.', '_')
dash.register_page(__name__, path=f'/GerenciarUsuario')
# require_login(__name__)


content_layout = dbc.Row(
    id=f'main-container-{page_name}',
    class_name='px-2 mx-0 shadow-lg',
    children=[

        # Titulo da pagina
        # Titulo().load(id='titulo-pagina', title_name='Gerenciar Usuário'),

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
                                            # dbc.Row(
                                            #   children=[
                                            #       dash_table.DataTable(
                                            #           id='table-dropdown',
                                            #           data=df_create_user.to_dict('records'),
                                            #           columns=[
                                            #               # {'id': 'Tipo de Usuário', 'name': 'Tipo de Usuário', 'presentation': 'dropdown'},
                                            #               {'id': 'Nome Completo', 'name': 'Nome Completo'},
                                            #               {'id': 'Email', 'name': 'Email', },
                                            #           ],
                                            #           editable=True,
                                            #           style_header={'textAlign': 'center', 'fontWeight': 'bold'},
                                            #           style_cell={'textAlign': 'center'},
                                            #             # dropdown={
                                            #             #     'Tipo de Usuário': {
                                            #             #         'options': [
                                            #             #             {'label': 'Tipo de Usuário', 'value': 'Gerente'},
                                            #             #             {'label': 'Tipo de Usuário', 'value': 'Admnistrativo'},
                                            #             #             {'label': 'Tipo de Usuário', 'value': 'Professor'},
                                            #             #             # for i in df_create_user['Tipo de Usuário'].unique
                                            #             #         ]
                                            #             #     },
                                            #             # }
                                            #         ),
                                            #   ]
                                            #
                                            # ),
                                            dbc.Row(
                                                class_name='col-lg-12 col-sm-12',
                                                # width=7,
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
                                                                            'Gerente': f'1: Gerente'.upper(),
                                                                            'Administrativo': f'2: Administrativo'.upper(),
                                                                            'Professor': f'3: Professor'.upper(),
                                                                        },
                                                                    )
                                                                ],
                                                                class_name='col-lg-12 col-sm-12 my-2'
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Col(
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
                                                                            '1': f'1: Ativo'.upper(),
                                                                            '0': f'2: Inativo'.upper(),
                                                                        },
                                                                    )
                                                                ],
                                                                class_name='col-lg-12 col-sm-12 my-2'
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Row(
                                                                id='button_area',
                                                                class_name='d-grid d-md-block',  # gap-2
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-create-user-{page_name}',
                                                                                children=['Salvar novo usuário'],
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
                                        style={'background-color': '#ffffff'},
                                        title="Criar Usuário do Sistema"
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
                                                                        children=[]
                                                                    ),
                                                                    dbc.Row(
                                                                        children=[
dbc.Row(
                                                        children=[
                                                            dbc.Row(
                                                                id='button_area',
                                                                class_name='d-grid d-md-block',  # gap-2
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-salvar-func-{page_name}',
                                                                                children=['Salvar Alterações'],
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
                                                ],
                                            ),
                                        ],
                                        style={'background-color': '#ffffff'},
                                        title="Criar Funcinário"
                                    )
                                ], start_collapsed=True, flush=True, style={'background-color': '#ffffff'}
                            ),
                        ], class_name=''
                    )
                ]
            ),
        dbc.Alert(id=f'out-alert-user-{page_name}'),
        ]
        )
#     ]
# )


def layout():
    try:
        if current_user.is_authenticated and dependecies.user_is_admin_or_gerente(session['email']):
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
                'nome_completo': [user_name],
                'tipo': [user_type],
                'status': [user_status],
            }
        )

        try:
            dados.insert_into_table(df=df_new_user, table_name='user')
            msg = 'Usuário Criado'
        except Exception as err:
            msg = f'{err}'

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


# @callback(
#     Output(component_id=f'out-alert-user-{page_name}', component_property='children'),
#     State(component_id=f'data-table-form-{page_name}',  component_property='data'),
#     Input(component_id=f'bt-save-func-{page_name}',  component_property='n_clicks'),
# )
# def salvar_funcionarios_editados(active_cell):
#     print(active_cell)
#     return str(active_cell) if active_cell else "Click the table"


@callback(
    Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),

    Input(component_id=f'main-container-{page_name}', component_property='children'),
)
def capturar_funcionarios(main_contianer):
    config = Config().config
    dados = Dados(config['ambiente'])

    df_user  = dados.query_table(
        table_name='user',
        field_list=[
            {'name': 'email'},
            {'name': 'nome_completo'},
            {'name': 'tipo'},
            {'name': 'status'},
        ]
    )
    df = df_user[df_user['tipo'].isin(['Gerente', 'Professor'])]

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

    # # Criando visualização em dashDataTable dos dados formatados
    dt_func = dash_table.DataTable(
        id=f'data-table-edit-func-{page_name}',
        data=df.to_dict('records'),
        columns=[{"name": i.upper(), "id": i} for i in df.columns],
        page_current=0,
        page_size=20,
        style_cell={'textAlign': 'center'},
        editable=False,
        filter_action='native',
        sort_mode="multi",
        sort_action="native",
        page_action="native",
        row_selectable="single",
        # row_selectable="multi",
        style_header={'textAlign': 'center', 'fontWeight': 'bold'},

    )
    datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    return datatable1