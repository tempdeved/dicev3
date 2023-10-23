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
page_name = 'LancarNotaTurma'
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
                                                        label="LANÇAR NOTA",
                                                        children=[
                                                            dbc.Row(id=f'out-edit-func-{page_name}'),
                                                            dbc.Row(
                                                                class_name='ml-0 pt-2',
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
                                                                                children=['SALVAR TURMA'],
                                                                                class_name='me-1',
                                                                                color='primary',
                                                                                n_clicks=0,
                                                                                disabled=True
                                                                            ),
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

        df_turma = pd.DataFrame(data_drom_data_table)

        turma_id = df_turma['id'].iloc[active_cell[0]]
        id_dice = int(df_turma['id_turma'].iloc[active_cell[0]])

        df_turma2  = dados.query_table(
            table_name='turma',
            # field_list=[
            #     {'name': 'email'},
            # ]
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
            #     {'name': 'email'},
            # ]
            # filter_list=[
            #     {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
            # ]
        )

        hist_columns = {
            # 'id':
            #     {'nome': 'id', 'type': 'nmeric, 'editableu: 1'},
            # 'created_at':
            #     {'nome': 'created_at', 'type': '', 'editable': 1},
            'id_turma':
                {'nome': 'id_turma', 'type': '', 'editable': 0},
            'id_aluno':
                {'nome': 'id_aluno', 'type': '', 'editable': 0},
            'numero_aulas':
                {'nome': 'numero_aulas', 'type': '', 'editable': 1},
            'numero_faltas':
                {'nome': 'numero_faltas', 'type': '', 'editable': 1},
            'research_01':
                {'nome': 'research_01', 'type': '', 'editable': 1},
            'organization_01':
                {'nome': 'organization_01', 'type': '', 'editable': 1},
            'interest_01':
                {'nome': 'interest_01', 'type': '', 'editable': 1},
            'group_activity_01':
                {'nome': 'group_activity_01', 'type': '', 'editable': 1},
            'speaking_01':
                {'nome': 'speaking_01', 'type': '', 'editable': 1},
            'frequencia_of_01':
                {'nome': 'frequencia_of_01', 'type': '', 'editable': 1},
            'listening_01':
                {'nome': 'listening_01', 'type': '', 'editable': 1},
            'readind_inter_01':
                {'nome': 'readind_inter_01', 'type': '', 'editable': 1},
            'writing_process_01':
                {'nome': 'writing_process_01', 'type': '', 'editable': 1},
            # 'descricao':
            #     {'nome': 'descricao', 'type': '', 'editable}: 1,
        }

        list_columns = [x for x in hist_columns]

        df_hist_turma  = dados.query_table(
            table_name='historico_aluno',
            # field_list=[
            #     {'name': 'email'},
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': f'{turma_id}'},
            ]
        )

        aux = pd.DataFrame(
            data={
                'id_aluno': list_alunos
            }
        )

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
            left=aux,
            right=df_hist_turma,
            how='left',
            on=['id_aluno'],
        )
        df_merge['id_turma'] = id_dice

        dt_turma = dash_table.DataTable(
            id=f'data-table-hist-aluno-{page_name}',
            data=df_merge[list_columns].to_dict('records'),
            columns=[
                {
                    "name": hist_columns[i]['nome'].replace('_', ' ').upper(),
                    "id": hist_columns[i]['nome'],
                    "type": hist_columns[i]['type'],
                    "editable": True if hist_columns[i]['editable'] == 1 else False,
                    "presentation": 'dropdown' if i == 'cadastrado' else '',
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
            style_cell={'textAlign': 'center'},
            page_size=30,
            filter_action='native',
            sort_mode="multi",
            sort_action="native",
            page_action="native",
            # editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},

        )



        datatable1 = dbc.Row(
            children=[
                dt_turma
            ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0'
        )
    else:

        dt_func = dash_table.DataTable(id=f'data-table-edit-func-{page_name}',)

        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0')

    return datatable1, '' if active_cell else ""


# id=f'out-alert-edited-fuc-{page_name}'

@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
    # State(component_id=f'data-table-edit-func-1-{page_name}',  component_property='data'),
    State(component_id=f'data-table-edit-func-5-{page_name}',  component_property='data'),
    State(component_id=f'data-table-edit-profs-{page_name}',  component_property='data'),
    # State(component_id=f'data-table-edit-func-3-{page_name}',  component_property='data'),
    State(component_id=f'inp-create-nivel-turma-{page_name}',  component_property='value'),
    State(component_id=f'inp-create-map-turma-{page_name}',  component_property='value'),
    State(component_id=f'id-turma-dice-{page_name}',  component_property='value'),
    # State(component_id=f'id-turma-dice-{page_name}',  component_property='value'),

    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
    )
def salvar_turma(dt_aluno, dt_prof, nivel, map, id_turma_dice, n_clicks):
    # if n_clicks :
    if n_clicks or dt_aluno or dt_prof or nivel or map:

        df_prof = pd.DataFrame(dt_prof)
        df_aluno = pd.DataFrame(dt_aluno)

        profs_cadastrados = df_prof[df_prof['cadastrado'] == 'CAD']
        alunos_cadastrados = df_aluno[df_aluno['cadastrado'] == 'CAD']

        df_turma = pd.DataFrame()
        df_turma['id'] = [6]
        df_turma['id_turma'] = [id_turma_dice]
        df_turma['nivel'] = [nivel]
        df_turma['map'] = [map]

        # append alunos novos
        if len(alunos_cadastrados) >=1 :
            list_aluno = []
            for x in alunos_cadastrados['id']:
                list_aluno.append(x)

            df_turma['id_aluno'] = json.dumps({'id_aluno': list_aluno})

        # append prof novos
        if len(profs_cadastrados) >= 1:
            func_prof = dados.query_table(
                table_name='funcionario',
                filter_list=[
                    {'op': 'in', 'name': 'id', 'value': profs_cadastrados['id'].to_list()}
                ],
            )


            list_profs = []
            for x in func_prof['email_func']:
                list_profs.append(x)

            df_turma['id_professor'] = json.dumps({'email_user': list_profs})

        try:
            dados.update_table(
                values=df_turma.to_dict(orient='records')[0],
                table_name='turma',
                pk_value=id_turma_dice,
                pk_name='id_turma'
            )

            return 'TURMA ATUALIZADA'
        except Exception as err:
            return str(err)

    else:
        return "SELECIONE UMA TURMA"