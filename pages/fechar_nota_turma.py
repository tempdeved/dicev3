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
from elements.check_list import RadioItem, CheckList

from banco.dados import Dados
from config.config import Config

# page_name = __name__[6:].replace('.', '_')
page_name = 'FecharTurma'
dash.register_page(__name__, path=f'/{page_name}')
# require_login(__name__)

config = Config().config
dados = Dados(config['ambiente'])

select_periodo = CheckList(
    id_object=f"mes-ref-{page_name}",
    title='PERÍODO',
    options=[
        {"label": "1° Sem", "value": 1, "disabled": True},
        {"label": "2° Sem", "value": 2, "disabled": True},
    ],
    inline=True,
    value=[1, 2, 3, 4],
    # disabled=True,
)
select_periodo.load()

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

                                            select_periodo.layout,

                                            # dbc.Row("PERÍODO", class_name='pt-2',),
                                            # dbc.RadioItems(
                                            #     id=f"mes-ref-{page_name}",
                                            #     options=[
                                            #         {"label": "Março/Abril", "value": 1},
                                            #         {"label": "Maio/Junho", "value": 2},
                                            #         {"label": "Ago/set", "value": 3},
                                            #         {"label": "Out/nov", "value": 4},
                                            #     ],
                                            #     value=1,
                                            #     inline=True,
                                            # ),

                                            dbc.Tabs(
                                                children=[
                                                    dbc.Tab(
                                                        id=f'tab-lancar-nt-{page_name}',
                                                        label="LANÇAR NOTA",
                                                        children=[
                                                            dbc.Row(

                                                            ),
                                                            dbc.Row(id=f'out-edit-func-{page_name}'),
                                                            dbc.Row(
                                                                class_name='ml-0 pt-2',
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-salvar-func-edited-{page_name}',
                                                                                children=['FECHAR TURMA'],
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
    Output(component_id=f'tab-lancar-nt-{page_name}', component_property='label'),
    State(component_id=f'data-table-edit-user-{page_name}',  component_property='data'),
    Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
    State(component_id=f"mes-ref-{page_name}",  component_property='value'),
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
            filter_list=[
                {'op': 'in', 'name': 'id', 'value': list_alunos},
            ]
        )

        df_all_aluno.rename(columns={'id': 'id_aluno'}, inplace=True)

        hist_columns = {
            # 'id':
            #     {'nome': 'id', 'type': 'nmeric, 'editableu: 1'},
            # 'created_at':
            #     {'nome': 'created_at', 'type': '', 'editable': 1},
            'id_turma':
                {'nome': 'id_turma', 'type': '', 'editable': 0},
            'id_aluno':
                {'nome': 'id_aluno', 'type': '', 'editable': 0},
            'nome':
                {'nome': 'nome', 'type': '', 'editable': 0},
            # 'numero_aulas':
            #     {'nome': 'numero_aulas', 'type': 'numeric', 'editable': 1},
            # 'numero_faltas':
            #     {'nome': 'numero_faltas', 'type': 'numeric', 'editable': 1},
            # 'research':
            #     {'nome': 'research', 'type': 'numeric', 'editable': 1},
            # 'organization':
            #     {'nome': 'organization', 'type': 'numeric', 'editable': 1},
            # 'interest':
            #     {'nome': 'interest', 'type': 'numeric', 'editable': 1},
            # 'group_activity':
            #     {'nome': 'group_activity', 'type': 'numeric', 'editable': 1},
            # 'speaking':
            #     {'nome': 'speaking', 'type': 'numeric', 'editable': 1},
            # 'frequencia_of':
            #     {'nome': 'frequencia_of', 'type': 'numeric', 'editable': 1},
            # 'listening':
            #     {'nome': 'listening', 'type': 'numeric', 'editable': 1},
            # 'readind_inter':
            #     {'nome': 'readind_inter', 'type': 'numeric', 'editable': 1},
            # 'writing_process':
            #     {'nome': 'writing_process', 'type': 'numeric', 'editable': 1},
            'frequency_pct':
                {'nome': 'frequencia_pct', 'type': 'numeric', 'editable': 0},
            # 'frequency':
            #     {'nome': 'frequencia_nt', 'type': 'numeric', 'editable': 0},
            'media':
                {'nome': 'media', 'type': 'numeric', 'editable': 0},
            # 'descricao':
            #     {'nome': 'descricao', 'type': '', 'editable}: 1,
        }

        list_columns = [x for x in hist_columns]

        df_result = pd.DataFrame(
            data={
                'id_aluno': df_all_aluno['id_aluno'],
                'nome': df_all_aluno['nome'],
            }
        )

        for int_month in mes_ref:

            df_hist_turma  = dados.query_table(
                table_name='historico_aluno',
                # field_list=[
                #     {'name': 'email'},
                # ]
                filter_list=[
                    {'op': 'eq', 'name': 'id_turma', 'value': int(turma_id_dice)},
                    # {'op': 'in', 'name': 'mes_ref', 'value': mes_ref},
                    {'op': 'eq', 'name': 'mes_ref', 'value': int(int_month)},
                ]
            )

            if df_hist_turma.empty:
                print(int_month)
            else:

                df_merge = pd.merge(
                    left=df_all_aluno,
                    right=df_hist_turma,
                    how='left',
                    on=['id_aluno'],
                )
                df_merge['id_turma'] = id_turma_dice
                df_merge['frequency_pct'] = 1 - (df_merge['numero_faltas'] / df_merge['numero_aulas'])
                df_merge['frequency'] = df_merge['frequency_pct'] * 100
                df_merge['frequency_pct'] = df_merge['frequency_pct'] * 100

                df_merge['frequency_pct'] = df_merge['frequency_pct'].apply(
                    lambda x: f'{x} %',
                )

                materias = [
                    'research',
                    'organization',
                    'interest',
                    'group_activity',
                    'speaking',
                    'frequencia_of',
                    'listening',
                    'readind_inter',
                    'writing_process',
                    'frequency'
                ]

                notas = []
                for idx, row in df_merge.iterrows():
                    # print(f'- {row["id_aluno"]}')

                    aux = 0
                    for mm in materias:
                        # print(mm)
                        # print(row[mm])

                        aux = aux + row[mm]

                    notas.append(
                        round(
                            (aux / len(materias)),
                            2
                        )
                    )

                meses_ref = {
                    1: "Março/Abril",
                    2: "Maio/Junho",
                    3: "Ago/set",
                    4: "Out/nov",
                }
                month_str = meses_ref[int_month]
                df_merge[f'media_{month_str}'] = notas

                df_result[f'freq_{month_str}'.upper()] = df_merge['frequency_pct']
                # df_result[f'freq_nt_{month_str}'.upper()] = df_merge['frequency']
                df_result[f'media_{month_str}'.upper()] = df_merge[f'media_{month_str}']

        """
        fim for
        """

        """
        ordenando tabela
        """
        df_result2 = pd.DataFrame(
            data={
                'id_turma': [turma_id_dice for x in range(0, len(df_result))],
                'id_aluno': df_result['id_aluno'],
                'nome': df_result['nome'],
            }
        )

        for col in df_result.columns:
            if 'FREQ' in col:
                df_result2[col] = df_result[col]
        # for col in df_result.columns:
        #     if 'FREQ_NT' in col:
        #         df_result2[col] = df_result[col]
        for col in df_result.columns:
            if 'MEDIA' in col:
                df_result2[col] = df_result[col]

        columns = [
            {
                "id": i,
                "name": i.replace('_', ' ').upper(),
                # "type": i,
                # "editable": True if hist_columns[i]['editable'] == 1 else False,
                # "presentation": 'dropdown' if i == 'cadastrado' else '',
            } for i in df_result2.columns
        ]

        df_result2['nome'] = df_result2['nome'].apply(
            lambda x: f'{x.split(" ")[0]} {x.split(" ")[1]}' if len(x.split(" ")) > 2 else f'{x.split(" ")[0]}'
        )

        dt_turma = dash_table.DataTable(
            id=f'data-table-hist-aluno-{page_name}',
            data=df_result2.to_dict('records'),
            # data=df_merge[list_columns].to_dict('records'),
            columns=columns,
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
            fixed_columns={'headers': True, 'data': 3},
            style_table={'minWidth': '100%'},
            style_cell={
                # all three widths are needed
                'textAlign': 'center',
                # 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_cell_conditional=[
                {'if': {'column_id': 'id_turma'}, 'width': '3%'},
                {'if': {'column_id': 'id_aluno'}, 'width': '3%'},
                {'if': {'column_id': 'nome'}, 'width': '5%'},
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


    # caputra mes ref STR
    meses_ref = {
        1: "Março/Abril",
        2: "Maio/Junho",
        3: "Ago/set",
        4: "Out/nov",
    }

    month_ref = f'NOTA'

    return datatable1, '', month_ref
    # return datatable1, '', month_ref if active_cell else ""


# id=f'out-alert-edited-fuc-{page_name}'

@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
    # State(component_id=f'data-table-edit-func-1-{page_name}',  component_property='data'),
    State(component_id=f'data-table-hist-aluno-{page_name}',  component_property='data'),
    # State(component_id=f'data-table-edit-profs-{page_name}',  component_property='data'),
    # State(component_id=f'data-table-edit-func-3-{page_name}',  component_property='data'),
    # State(component_id=f'inp-create-nivel-turma-{page_name}',  component_property='value'),
    # State(component_id=f'inp-create-map-turma-{page_name}',  component_property='value'),
    # State(component_id=f'id-turma-dice-{page_name}',  component_property='value'),
    # State(component_id=f"mes-ref-{page_name}",  component_property='value'),

    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
    )
def salvar_nota_turma(dt_notas, n_clicks):
    # if n_clicks :
    if n_clicks:

        df_notas = pd.DataFrame(dt_notas)
        id_turma = int(df_notas['id_turma'].unique()[0])

        try:
            # removendo notas para inserir novas notas
            dados.update_table(
                values={
                    'id_turma': id_turma,
                    'status': f'finalizada'.upper()
                },
                table_name='turma',
                pk_value=id_turma,
                pk_name='id_turma'
            )

            return f'TURMA FINALIZADA'
        except Exception as err:
            return str(err)

    else:
        return "SELECIONE UMA TURMA"