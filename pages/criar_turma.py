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
dash.register_page(__name__, path=f'/CriarTurma')
# require_login(__name__)


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
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-create-user-{page_name}',
                                                                                children=['SALVAR TURMA'],
                                                                                class_name='me-0',
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
                                        className='m-0 p-0',
                                        style={'background-color': '#ffffff'},
                                        title="CRIAR TURMA"
                                    )
                                ],
                                className='m-0 p-0',
                                start_collapsed=True,
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
    Output(component_id=f'out-form-turma-{page_name}', component_property='children'),
    Input(component_id=f'main-container-{page_name}', component_property='children'),
)
def update_datepicker(datepicker):
    # result = dcc.DatePickerSingle(
    #     id=f'inp-date-inicio-aluno-{page_name}',
    #     min_date_allowed=datetime.date(1992, 8, 12),
    #     # max_date_allowed=datetime.,
    #     initial_visible_month=datetime.datetime.today(),
    #     # date=datetime.datetime.today(),
    #     month_format='MMMM Y',
    #     display_format='DD-MM-YYYY',
    #     # placeholder='YY-MM-DD',
    # )

    config = Config().config
    dados = Dados(config['ambiente'])

    df_horario = dados.query_table(table_name='horario')
    df_user = dados.query_table(table_name='user')
    df_funcionario = dados.query_table(table_name='funcionario')
    df_aluno = dados.query_table(table_name='aluno')

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
            'label': f'{row["dia_semana"]} de {row["hora_inicio"].zfill(2)}:{row["hora_inicio"].zfill(2)} até ' 
                     f'{row["hora_fim"].zfill(2)}:{row["min_fim"].zfill(2)}',
            'value': row["id"]
        }
        for i, row in df_horario.iterrows()
    ]

    df_professor['nome_completo']

    professor_lista = [
        {
            'label': f'{row["nome_completo"]} {row["status"]} ',
            'value': row["email"]
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
        className='m-0 p-0',
    )

    result = dbc.Row(
        children=[
            row_horario
        ],
        className='m-0 p-0',
    )


    return result

@callback(
    Output(component_id=f'out-alert-user-{page_name}', component_property='children'),

    # State(component_id=f'inp-create-min-fim-{page_name}', component_property='value'),

    Input(component_id=f'btn-create-user-{page_name}', component_property='n_clicks'),
)
def create_horario(n_clicks):

    if n_clicks:
    # if user_type and user_name and user_email and user_passdw:
        config = Config().config
        dados = Dados(config['ambiente'])

        df_new_horario= pd.DataFrame(
            data={
                'dia_semana': [dia_semana],
                'hora_inicio': [hora_inicio],
                'min_inicio': [min_inicio],
                'hora_fim': [hora_fim],
                'min_fim': [min_fim],
            }
        )
        try:
            df_new_horario.dropna(inplace=True)
            dados.insert_into_table(df=df_new_horario, table_name='horario')
            msg = 'Usuário Criado'
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


@callback(
    Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),

    Input(component_id=f'btn-buscar-usuarios-{page_name}', component_property='n_clicks'),
)
def capturar_funcionarios(main_contianer):

    if main_contianer >= 1:

        config = Config().config
        dados = Dados(config['ambiente'])

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

        df = df_merge[df_merge['tipo'].isin(['Professor', 'Gerente'])]

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
            page_size=5,
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
        config = Config().config
        dados = Dados(config['ambiente'])

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

        )

        dt_func2 = dash_table.DataTable(
            id=f'data-table-edit-func-2-{page_name}',
            data=df_func2.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_func2.columns],
            style_cell={'textAlign': 'center'},
            editable=True,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )
        dt_func3 = dash_table.DataTable(
            id=f'data-table-edit-func-3-{page_name}',
            data=df_func3.to_dict('records'),
            columns=[{"name": i.upper(), "id": i} for i in df_func3.columns],
            style_cell={'textAlign': 'center'},
            editable=True,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

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