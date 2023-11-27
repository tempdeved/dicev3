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
page_name = 'Remarks'
dash.register_page(__name__, path=f'/{page_name}')
# require_login(__name__)

config = Config().config
dados = Dados(config['ambiente'])

content_layout = dbc.Row(
    id=f'main-container-{page_name}',
    # class_name='px-2 mx-0 shadow-lg',
    # class_name='col-lg-10',
    children=[
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
                                                id=f'out-edit-funcionario-{page_name}',
                                                children=[
                                                    dash_table.DataTable(
                                                        id=f'data-table-edit-user-{page_name}',
                                                    ),
                                                ]
                                            ),

                                            dbc.Row("PERÍODO", class_name='pt-2',),
                                            dbc.RadioItems(
                                                id=f"mes-ref-{page_name}",
                                                options=[
                                                    {"label": "Março/Abril", "value": 1},
                                                    {"label": "Maio/Junho", "value": 2},
                                                    {"label": "Ago/set", "value": 3},
                                                    {"label": "Out/nov", "value": 4},
                                                ],
                                                value=1,
                                                inline=True,
                                            ),

                                            dbc.Tabs(
                                                children=[
                                                    dbc.Tab(
                                                        label="REMARK",
                                                        children=[
                                                            dbc.Row(

                                                            ),
                                                            dbc.Row(id=f'out-edit-func-{page_name}'),
                                                            dbc.Row(),
                                                            dbc.Row(id=f'out-remark-edit{page_name}'),
                                                            dbc.Row(
                                                                class_name='ml-0 pt-2',
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-salvar-func-edited-{page_name}',
                                                                                children=['SALVAR REMARK'],
                                                                                class_name='me-1',
                                                                                color='primary',
                                                                                n_clicks=0,
                                                                                disabled=False
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
                        dependecies.is_administrativo_user(session['email']) or
                        dependecies.is_professor_user(session['email'])
                ):
                return content_layout
    except Exception as err:
        # return login_layout()
        # return redirect('/')
        return Titulo().load(id='titulo-pagina', title_name='Sem permissão')
    return Titulo().load(id='titulo-pagina', title_name='Sem permissão')



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
            {'name': 'semestre'},
            {'name': 'status'},
            {'name': 'nivel'},
            {'name': 'inicio'},
            {'name': 'fim'},
            {'name': 'map'},
            {'name': 'idioma'},
        ]
    )

    df_turma.sort_values(
        by=['id', 'status', 'semestre'],
        ascending=[False, True, True],
        inplace=True
    )
    colulmn_type = {
        'id': 'numeric',
        'id_turma': 'numeric',
        'semestre': 'text',
        'status': 'text',
        'nivel': 'text',
        'inicio': 'text',
        'fim': 'text',
        'map': 'text',
        'idioma': 'text',
    }

    dt_user = dash_table.DataTable(
        id=f'data-table-edit-user-{page_name}',
        data=df_turma.to_dict('records'),
        columns=[
            {
                "name": i.replace('_', ' ').upper(),
                "id": i,
                'type': colulmn_type[i]
            } for i in df_turma.columns],
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
    datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    return datatable1

@callback(
    Output(component_id=f'out-edit-func-{page_name}', component_property='children'),
    Output(component_id=f'out-alert-fuc-{page_name}', component_property='children'),
    State(component_id=f'data-table-edit-user-{page_name}',  component_property='data'),
    Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
    Input(component_id=f"mes-ref-{page_name}",  component_property='value'),
    # prevent_initial_callbacks=True,
    )
def editar_turma(data_drom_data_table, active_cell, mes_ref):

    if data_drom_data_table and active_cell:

        df_turma = pd.DataFrame(data_drom_data_table)

        turma_id = df_turma['id'].iloc[active_cell[0]]
        turma_id_dice = df_turma['id_turma'].iloc[active_cell[0]]
        id_turma_dice = int(df_turma['id_turma'].iloc[active_cell[0]])

        df_turma2  = dados.query_table(
            table_name='turma',
            # field_list=[
            #     {'name': 'email'},
            # ],
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
            ]
        )

        if len(df_turma2['id_aluno']) >= 1:
            print('possui alunos')
        else:
            print('nao possui')
            return 'não possui alunos cadastrados'

        list_alunos = json.loads(df_turma2['id_aluno'][0])['id_aluno']

        df_all_aluno  = dados.query_table(
            table_name='aluno',
            # field_list=[
            #     {'name': 'descricao'},
            # ],
            filter_list=[
                {'op': 'in', 'name': 'id', 'value': list_alunos},
            ]
        )

        hist_columns = {
            # 'id':
            #     {'nome': 'id', 'type': 'nmeric, 'editableu: 1'},
            # 'created_at':
            #     {'nome': 'created_at', 'type': '', 'editable': 1},
            # 'id_turma':
            #     {'nome': 'id_turma', 'type': '', 'editable': 0, 'width': '600px'},
            'id_hist':
                {'nome': 'id_hist', 'type': '', 'editable': 0, 'width': '600px'},
            'nome':
                {'nome': 'nome', 'type': '', 'editable': 0, 'width': '600px'},
            # 'descricao':
            #     {'nome': 'descricao', 'type': '', 'editable': 1, 'width': '50px'},
        }

        list_columns = [x for x in hist_columns]

        df_hist_turma  = dados.query_table(
            table_name='historico_aluno',
            field_list=[
                {'name': 'id'},
                {'name': 'id_aluno'},
                {'name': 'descricao'},
            ],
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': int(turma_id_dice)},
                {'op': 'eq', 'name': 'mes_ref', 'value': int(mes_ref)},
            ]
        )
        df_hist_turma.rename(columns={'id':'id_hist'}, inplace=True)

        # aux = pd.DataFrame(
        #     data={
        #         'id_aluno': list_alunos
        #     }
        # )

        df_all_aluno.rename(columns={'id': 'id_aluno'}, inplace=True)

        # if len(df_hist_turma >= 1):
        #     print('contem historico')
        #
        #     merge = pd.merge(
        #         left=aux,
        #         right=df_hist_turma,
        #         how='left',
        #         on=['id_aluno'],
        #     )
        #
        # #     append em list_alunos
        # else:
        #     print('turma nao contem historico')
        #     merge = aux.copy

        df_merge = pd.merge(
            left=df_all_aluno,
            right=df_hist_turma,
            how='left',
            on=['id_aluno'],
        )
        df_merge['id_turma'] = id_turma_dice

        dt_turma = dash_table.DataTable(
            id=f'data-table-hist-aluno-{page_name}',
            data=df_merge[list_columns].to_dict('records'),
            columns=[
                {
                    "name": hist_columns[i]['nome'].replace('_', ' ').upper(),
                    "id": hist_columns[i]['nome'],
                    "type": hist_columns[i]['type'],
                    "editable": True if hist_columns[i]['editable'] == 1 else False,
                    # "presentation": 'dropdown' if i == 'cadastrado' else '',
                 } for i in list_columns
            ],
            # dropdown={
            #     'cadastrado': {
            #         'options': [
            #             {'label': "CAD", 'value': "CAD"},
            #             {'label': "NAO CAD", 'value': "NAO CAD"},
            #         ]
            #     }
            # },
            # style_cell={'textAlign': 'center'},
            page_size=30,
            filter_action='native',
            sort_mode="multi",
            sort_action="native",
            page_action="native",
            # editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,
            style_data={
                'whiteSpace': 'normal',
                # 'height': 'auto'
            },
            # fixed_columns={'headers': True, 'data': 3},
            # style_table={'minWidth': '100%'},
            style_cell={
                # all three widths are needed
                'textAlign': 'center',
                # 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                # 'overflow': 'hidden',
                # 'textOverflow': 'ellipsis',
                # 'word-wrap': 'break-word'
            },
            row_selectable="single",
            style_cell_conditional=[
                {
                    'if': {'column_id': hist_columns[i]['nome'].replace('_', ' ').upper()},
                    'width': hist_columns[i]['width'],
                    # 'textOverflow': hist_columns[i]['textOverflow']
                } for i in list_columns
            ]

        )


        datatable1 = dbc.Row(
            children=[
                dt_turma
            ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 overflow-auto'
        )
        # datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    else:

        dt_func = dash_table.DataTable(id=f'data-table-edit-func-{page_name}',)

        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 overflow-auto')

    return datatable1, '' if active_cell else ""


@callback(
    Output(component_id=f'out-remark-edit{page_name}', component_property='children'),
    State(component_id=f"mes-ref-{page_name}", component_property='value'),
    State(component_id=f'data-table-edit-user-{page_name}', component_property='data'),
    State(component_id=f'data-table-hist-aluno-{page_name}', component_property='data'),
    Input(component_id=f'data-table-hist-aluno-{page_name}', component_property='selected_rows'),
)
def edit_remart(mes_ref, dt_turma, dt_alu_tur, active_cell):

    if dt_alu_tur and active_cell:
        df_alu_turma = pd.DataFrame(dt_alu_tur)
        df_turma = pd.DataFrame(dt_turma)

        # turma_id =  df_turma['id_turma'].iloc[active_cell[0]]
        # turma_id_dice = df_turma['id_turma'].iloc[active_cell[0]]
        id_hist = int(df_alu_turma['id_hist'].iloc[active_cell[0]])
        nome_aluno = str(df_alu_turma['nome'].iloc[active_cell[0]])

        df_hist_turma  = dados.query_table(
            table_name='historico_aluno',
            field_list=[
                {'name': 'id'},
                {'name': 'descricao'},
            ],
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': int(id_hist)},
            ]
        )
        descricao = df_hist_turma['descricao'][0]

        editable_remark = dbc.Row(
            children=[
                dbc.Row(
                    children=[
                     html.H1(nome_aluno)
                    ],
                    className='pt-5',
                    style={
                        'background-color': '#ffffff'
                    },
                ),
                dbc.Row(children=[
                    dbc.Textarea(
                        id=f"aluno-descricao-{page_name}",
                        size="lg",
                        placeholder="",
                        value=descricao,
                        style={
                            'width': '100%',
                            'height': '500px'
                        },


                    )
                ],
                    className='py-2'
                ),

            ],
        )
    else:
        editable_remark = ''

    return editable_remark


@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
    State(component_id=f'data-table-hist-aluno-{page_name}',  component_property='data'),
    State(component_id=f'data-table-hist-aluno-{page_name}', component_property='selected_rows'),
    State(component_id=f"mes-ref-{page_name}",  component_property='value'),
    State(component_id=f"aluno-descricao-{page_name}",  component_property='value'),

    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
    )
def salvar_nota_turma(dt_notas, active_cell, mes_ref, descricao, n_clicks):
    # if n_clicks :
    if n_clicks:

        df_hist = pd.DataFrame(dt_notas)

        id_hist = int(df_hist['id_hist'].iloc[active_cell[0]])
        nome_aluno = df_hist['nome'].iloc[active_cell[0]]

        df_notas = pd.DataFrame(
            data={
                'id': [id_hist],
                'descricao': [descricao],
            }
        )


        # df_notas['mes_ref'] = mes_ref
        # df_notas['created_at'] = datetime.datetime.now()
        # df_notas.fillna(0, inplace=True)

        # hist_alunos = dados.query_table(
        #     table_name='historico_aluno',
        #     filter_list=[
        #         {'op': 'eq', 'name': 'id_turma', 'value': int(df_notas['id_turma'].unique()[0])},
        #         {'op': 'eq', 'name': 'mes_ref', 'value': int(df_notas['mes_ref'].unique()[0])},
        #     ]
        # )

        try:
            # removendo notas para inserir novas notas
            # dados.remove_from_table(
            #     table_name='historico_aluno',
            #     filter_list=[
            #         {'op': 'in', 'name': 'id', 'value': hist_alunos['id'].to_list()},
            #     ]
            # );
            dados.update_table(
                values=df_notas.to_dict(orient='records')[0],
                table_name='historico_aluno',
                pk_value=id_hist,
                pk_name='id'
            )

            return f'{nome_aluno} ATUALIZADA'
        except Exception as err:
            return str(err)

    else:
        return "SELECIONE UMA TURMA"