import datetime
import dash
import mysql.connector.errors
import pandas as pd
import sqlalchemy.exc
import json
import dash_ag_grid as dag

from elements.check_list import CheckList, RadioItem
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

semestre = RadioItem(
            id_object=f"mes-ref-{page_name}",
            title='PERÍODO',
            options=[
                {"label": "Mar/Abr", "value": 1},
                {"label": "Mai/Jun", "value": 2},
                {"label": "Ago/Set", "value": 3},
                {"label": "Out/Nov", "value": 4},
            ],
            labelCheckedClassName="text-primary",
            inputCheckedClassName="border border-primary bg-primary",
            value=1,
            inline=True,
            switch=True,
        )
semestre.load()


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
                                                class_name='dbc',
                                                children=[
                                                    dash_table.DataTable(
                                                        id=f'data-table-edit-user-{page_name}',
                                                    ),
                                                ]
                                            ),

                                            # dbc.Row("PERÍODO", class_name='pt-2',),
                                            # dbc.RadioItems(
                                            #     id=f"mes-ref-{page_name}",
                                            #     options=[
                                            #         {"label": "1° Sem", "value": 1},
                                            #         {"label": "2° Sem", "value": 2},
                                            #     ],
                                            #     value=1,
                                            #     inline=True,
                                            # ),
                                            semestre.layout,

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
                                                                                children=['SALVAR TURMA'],
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

                                            # dbc.Row(id=f'out-edit-func-{page_name}'),

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
        by=['status', 'inicio', ],
        ascending=[True, False, ],
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
    datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0 dbc')

    return datatable1

@callback(
    Output(component_id=f'out-edit-func-{page_name}', component_property='children'),
    Output(component_id=f'out-alert-fuc-{page_name}', component_property='children'),
    Output(component_id=f'tab-lancar-nt-{page_name}', component_property='label'),
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
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
            ]
        )
        df_turma_aluno  = dados.query_table(
            table_name='turma_aluno',
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': id_turma_dice},
            ]
        )

        list_alunos = df_turma_aluno['id_aluno'].to_list()

        df_all_aluno  = dados.query_table(
            table_name='aluno',
            # field_list=[
            #     {'name': 'email'},
            # ]
            filter_list=[
                {'op': 'in', 'name': 'id', 'value': list_alunos},
            ]
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
            'nome':
                {'nome': 'nome', 'type': '', 'editable': 0},
            'numero_aulas':
                {'nome': 'numero_aulas', 'type': 'numeric', 'editable': 1},
            'numero_faltas':
                {'nome': 'numero_faltas', 'type': 'numeric', 'editable': 1},
            'research':
                {'nome': 'research', 'type': 'numeric', 'editable': 1},
            'organization':
                {'nome': 'organization', 'type': 'numeric', 'editable': 1},
            'interest':
                {'nome': 'interest', 'type': 'numeric', 'editable': 1},
            'group_activity':
                {'nome': 'group_activity', 'type': 'numeric', 'editable': 1},
            'speaking':
                {'nome': 'speaking', 'type': 'numeric', 'editable': 1},
            'frequencia_of':
                {'nome': 'frequencia_of', 'type': 'numeric', 'editable': 1},
            'listening':
                {'nome': 'listening', 'type': 'numeric', 'editable': 1},
            'readind_inter':
                {'nome': 'readind_inter', 'type': 'numeric', 'editable': 1},
            'writing_process':
                {'nome': 'writing_process', 'type': 'numeric', 'editable': 1},
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
                {'op': 'eq', 'name': 'id_turma', 'value': int(turma_id_dice)},
                {'op': 'eq', 'name': 'mes_ref', 'value': int(mes_ref)},
            ]
        )

        aux = pd.DataFrame(
            data={
                'id_aluno': list_alunos
            }
        )

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

        df_merge['nome'] = df_merge['nome'].apply(
            lambda x: f'{x.split(" ")[0]} {x.split(" ")[1]}' if len(x.split(" "))  > 2 else f'{x.split(" ")[0]}'
        )

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
            # style_cell={'textAlign': 'center'},
            page_size=30,
            # filter_action='native',
            # sort_mode="multi",
            # sort_action="native",
            # page_action="native",
            # editable=False,
            style_header={
                'textAlign': 'center',
                'fontWeight': 'bold',
                # 'transform': 'rotate(270deg)',
                # 'display': 'block'
            },
            # style_as_list_view=True,
            # fixed_columns={'headers': True, 'data': 3},
            # style_table={'minWidth': '100%'},
            style_cell={
                # all three widths are needed
                'textAlign': 'center',
                # 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                # 'overflow': 'hidden',
                # 'textOverflow': 'ellipsis',
                # 'transform': 'rotate(270deg)',
            },
            # style_cell_conditional=[
                # {'if': {'column_id': 'id_turma'}, 'width': '2%'},
                # {'if': {'column_id': 'id_aluno'}, 'width': '2%'},
                # {'if': {'column_id': 'nome'}, 'width': '3%'},
                # {'if': {'column_id': 'numero_aulas'}, 'transform': 'rotate(270deg);'},
                # {'if': {'column_id': 'numero_faltas'}, 'transform': 'rotate(270deg);'},
            # ],
        )
        # columns_datatable = [
        #     {
        #         "field": i,
        #         'headerName': columns[i]['name'],
        #         'filter': True,
        #         'editable': False,
        #         'type': columns[i]['type'],
        #         "filterParams": {
        #             "buttons": ["apply", "reset"],
        #             "closeOnApply": False,
        #         },
        #         "sortable": True,
        #         'valueFormatter': columns[i]['format'],
        #         'checkboxSelection': columns[i]['checkbox_selection'],
        #         'autoHeight': True,
        #         # 'rowGroup': columns[i]['group'],
        #         # 'aggFunc': columns[i]['aggFunc'],
        #         # 'hide': columns[i]['hide'],
        #         # 'pinned': columns[i]['pinned'],
        #         # 'floatingFilter': columns[i]['pinned'],
        #
        #     } for i in columns
        # ]



        columnDefs = [
            {
                "field": x,
                "headerName": config['lancar_nota_turma']['table_contraparte'][x]['headerName'].replace('_', ' ').title(),
                'suppressSizeToFit': config['lancar_nota_turma']['table_contraparte'][x]['suppressSizeToFit'],
                'editable': config['lancar_nota_turma']['table_contraparte'][x]['editable'],
                # 'width': 80,
                'width': config['lancar_nota_turma']['table_contraparte'][x]['width'],
            }
            for x in config['lancar_nota_turma']['table_contraparte']
        ]

        turma2 = dag.AgGrid(
            id=f'data-table-hist-aluno-{page_name}',
            columnDefs=columnDefs,
            rowData=df_merge[list_columns].to_dict('records'),
            dashGridOptions={
                # 'groupHeaderHeight': 120,
                'headerHeight': 150,
                # 'floatingFiltersHeight': 100,
                "animateRows": True,
                # "wrapHeaderText": True,
                # "autoHeaderHeight": True,
            },
            # defaultColDef={"editable": True, "filter": True, "floatingFilter": True},
            columnSize="sizeToFit",
        )

        datatable1 = dbc.Row(
            children=[
                # html.P('a'),
                # html.P('a'),
                # html.P('a'),
                # html.P('a'),
                # html.P('a'),
                # html.P('a'),
                # html.P('a'),

                # dt_turma,

                # html.Br('a'),
                # html.Br('a'),

                turma2,

                # html.Br('a'),
                # html.Br('a'),
                # html.Br('a'),
                # html.Br('a'),
                # html.Br('a'),
            ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 overflow-auto dbc dbc-ag-grid header1'
        )
        # datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    else:

        dt_func = dash_table.DataTable(id=f'data-table-edit-func-{page_name}',)

        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 dbc dbc-ag-grid overflow-auto')


    # caputra mes ref STR
    meses_ref = {
        1: "Mar/Abr",
        2: "Mai/Jun",
        3: "Ago/Set",
        4: "Out/Nov",
    }

    month_ref = f'LANÇAR NOTA - {meses_ref[mes_ref]}'

    return datatable1, '', month_ref
    # return datatable1, '', month_ref if active_cell else ""


# id=f'out-alert-edited-fuc-{page_name}'

@callback(
    Output(component_id=f'out-alert-edited-fuc-{page_name}', component_property='children'),
    # State(component_id=f'data-table-edit-func-1-{page_name}',  component_property='data'),
    State(component_id=f'data-table-hist-aluno-{page_name}',  component_property='rowData'),
    # State(component_id=f'data-table-edit-profs-{page_name}',  component_property='data'),
    # State(component_id=f'data-table-edit-func-3-{page_name}',  component_property='data'),
    # State(component_id=f'inp-create-nivel-turma-{page_name}',  component_property='value'),
    # State(component_id=f'inp-create-map-turma-{page_name}',  component_property='value'),
    # State(component_id=f'id-turma-dice-{page_name}',  component_property='value'),
    State(component_id=f"mes-ref-{page_name}",  component_property='value'),

    Input(component_id=f'btn-salvar-func-edited-{page_name}',  component_property='n_clicks'),
    )
def salvar_nota_turma(dt_notas, mes_ref, n_clicks):
    # if n_clicks :
    if n_clicks:

        df_notas = pd.DataFrame(dt_notas)
        df_notas['mes_ref'] = mes_ref
        df_notas['created_at'] = datetime.datetime.now()
        df_notas.fillna(0, inplace=True)

        hist_alunos = dados.query_table(
            table_name='historico_aluno',
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': int(df_notas['id_turma'].unique()[0])},
                {'op': 'eq', 'name': 'mes_ref', 'value': int(df_notas['mes_ref'].unique()[0])},
            ]
        )

        try:
            # removendo notas para inserir novas notas
            dados.remove_from_table(
                table_name='historico_aluno',
                filter_list=[
                    {'op': 'in', 'name': 'id', 'value': hist_alunos['id'].to_list()},
                ]
            )
            dados.insert_into_table(df=df_notas, table_name='historico_aluno')
            meses_ref = {
                1: "Mar/Abr",
                2: "Mai/Jun",
                3: "Ago/Set",
                4: "Out/Nov",
            }

            return f'TURMA ATUALIZADA {meses_ref[mes_ref]}'
        except Exception as err:
            return str(err)

    else:
        return "SELECIONE UMA TURMA"