import glob
import os.path
import datetime
import dash
import mysql.connector.errors
import pandas as pd
import sqlalchemy.exc
import json
import dash_ag_grid as dag

from utils.create_excel import Turma_xlsx

import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo
from elements.check_list import RadioItem, CheckList
from elements.dropdown import DropDownMenu
from string import Template
from utils.get_idade import CalculateAge

from banco.dados import Dados
from config.config import Config

# page_name = __name__[6:].replace('.', '_')
page_name = 'BoletimAluno'
dash.register_page(__name__, path=f'/{page_name}')
# require_login(__name__)

config = Config().config
dados = Dados(config['ambiente'])

select_periodo = RadioItem(
    id_object=f"mes-ref-{page_name}",
    title='PERÍODO',
    options=[
        {"label": "1° Sem.", "value": 1,},
        {"label": "2° Sem.", "value": 2,},
    ],
    labelCheckedClassName="text-primary",
    inputCheckedClassName="border border-primary bg-primary",
    value=1,
    inline=True,
    switch=True,
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
                                                children=[
                                                    dbc.Col(
                                                        id=f"load-turmas-{page_name}",
                                                        class_name='col-lg-2 col-md-12 col-sm-12',
                                                    ),
                                                    dbc.Col(
                                                        children=[
                                                            select_periodo.layout,
                                                        ],
                                                        class_name='col-lg-4 col-md-12 col-sm-12',
                                                    ),
                                                    dbc.Col(
                                                        id=f"load-alunos-{page_name}",
                                                        class_name='col-lg-6 col-md-12 col-sm-12',
                                                    ),
                                                ]
                                            ),

                                            # dbc.Row(
                                            #     id=f'out-edit-funcionario-{page_name}',
                                            #     children=[
                                            #         dash_table.DataTable(
                                            #             id=f'data-table-edit-user-{page_name}',
                                            #         ),
                                            #     ]
                                            # ),



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
                                                        label="BOLETIM",
                                                        class_name='w-100 ',
                                                        children=[

                                                            # retorno vazio da funcao JS de imprimpri
                                                            dbc.Row(id=f"notification-output-{page_name}"),

                                                            dbc.Row(
                                                                class_name='ml-0 pt-2',
                                                                children=[
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            dbc.Button(
                                                                                id=f'btn-imprimpir-generico-{page_name}',
                                                                                children=['IMPRIMIR'],
                                                                                class_name='me-0',
                                                                                color='primary',
                                                                                n_clicks=0,
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    dbc.Col(
                                                                        # width=2,
                                                                        children=[
                                                                            # dbc.Button(
                                                                            #     id=f'btn-download-turma-{page_name}',
                                                                            #     children=['DOWNLOAD P/ TURMA'],
                                                                            #     class_name='me-0',
                                                                            #     color='primary',
                                                                            #     n_clicks=0,
                                                                            # ),
                                                                            # dcc.Download(id=f"out-download-turma-{page_name}")
                                                                        ]
                                                                    ),
                                                                    # dbc.Col(
                                                                    #     # width=2,
                                                                    #     children=[
                                                                    #         html.A(
                                                                    #             dbc.Button(
                                                                    #                 id=f'btn-limpar-campos-{page_name}',
                                                                    #                 children=['LIMPAR CAMPOS'],
                                                                    #                 class_name='me-1',
                                                                    #                 color='light',
                                                                    #                 n_clicks=0,
                                                                    #
                                                                    #             ),
                                                                    #             href=f'/{page_name}'),
                                                                    #     ]
                                                                    # ),
                                                                ]
                                                            ),

                                                            dbc.Row(id=f"output-alunos-{page_name}"),

                                                            dbc.Row(id=f'out-edit-func-{page_name}'),

                                                            dbc.Collapse(
                                                                id=f'collapse-print-{page_name}',
                                                                children=[
                                                                    dbc.Row(
                                                                        id=f'out-edit-funcionario-print-{page_name}',
                                                                        children=[],
                                                                        class_name='p-0 m-0',
                                                                    ),
                                                                ],
                                                                is_open=False,
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

        # dbc.Alert(
        dbc.Row(
            children=[
                dbc.Row(id=f'out-alert-user-{page_name}'),
                dbc.Row(id=f'out-alert-fuc-{page_name}'),
                dbc.Row(id=f'out-alert-edited-fuc-{page_name}'),
                dbc.Row(id=f'out-alert-imp-aluno-{page_name}'),
            ],
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


print_page = f'out-edit-funcionario-print-{page_name}'

js_model_print = Template("""
function (n_clicks) {
        var page =  '$print_page'
        var n = n_clicks
        console.log('n')
        console.log(n)
        console.log('n_clicks')
        console.log(n_clicks)
        console.log(n + '- TESTE-----')

        var printContents = document.getElementById(page).innerHTML;
        var originalContents = document.body.innerHTML;

        document.body.innerHTML = printContents;

        window.print();

        document.body.innerHTML = originalContents;
        location.reload()

        return window.dash_clientside.no_update
    }
    """)


js_print = js_model_print.substitute(
    print_page=print_page
)

clientside_callback(
    js_print,
    Output(component_id=f"notification-output-{page_name}", component_property="children"),
    Input(component_id=f'btn-imprimpir-generico-{page_name}', component_property="n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output(component_id=f"load-turmas-{page_name}", component_property="children"),
    Input(component_id=f'main-container-{page_name}', component_property="n_clicks"),
)
def load_turmas(main):

    df_turmas = dados.query_table(table_name='turma')
    df_turmas.sort_values(by=['id_turma'], ascending=[False], inplace=True)
    options = [
        {'label': x, 'value': int(x)}
    for x in df_turmas['id_turma'].to_list()
    ]
    row_status = DropDownMenu(
        id_object=f'inp-turma-load-{page_name}',
        title='TURMA',
        options=options,
        value=int(df_turmas['id_turma'].max()),
    )
    row_status.load()

    return row_status.layout


@callback(
    Output(component_id=f"load-alunos-{page_name}", component_property="children"),
    Input(component_id=f'inp-turma-load-{page_name}', component_property="value"),
)
def load_alunos(id_turma):

    df_turmas = dados.query_table(
        table_name='turma_aluno',
        filter_list=[
            {'op': 'eq', 'name': 'id_turma', 'value': int(id_turma)},
        ]
    ).drop(columns=['id'])

    df_aluno = dados.query_table(
        table_name='aluno',
    ).rename(
        columns={'id':'id_aluno'}
    )

    df_merge = pd.merge(
        left=df_turmas,
        right=df_aluno,
        how='left',
        on=['id_aluno']
    )

    # df_turmas.sort_values(by=['id_turma'], ascending=[False], inplace=True)
    options = [
        {'label': f"{row['id_aluno']} - {row['nome']} ", 'value': row['id_aluno']}
    for indx, row in df_merge.iterrows()
    ]
    row_status = DropDownMenu(
        id_object=f'inp-alunos-load-{page_name}',
        title='ALUNOS',
        options=options,
        value=df_merge['id_aluno'].max(),
    )
    row_status.load()

    return row_status.layout

@callback(
    Output(component_id=f"out-download-turma-{page_name}", component_property="data"),
    State(component_id=f'data-table-hist-aluno-{page_name}', component_property="data"),
    # State(component_id=f'data-table-edit-user-{page_name}', component_property="data"),
    Input(component_id=f'btn-download-turma-{page_name}', component_property="n_clicks"),
    prevent_initial_call=True,
)
def func(df_raw, n_clicks):
    if df_raw:
        path_folder = 'download'
        filename = page_name + '.xlsx'
        file_path = os.path.join(path_folder, filename)


        # delete xlsx files
        for f in glob.iglob(path_folder + '/*.xlsx', recursive=True):
            os.remove(f)

        df = pd.DataFrame(data=df_raw)

        # create file
        Turma_xlsx(file_path=file_path, df=df)

        # return file
        return dcc.send_file(file_path)

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
        # row_selectable="single",
        row_selectable="single",
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
    # Output(component_id=f'out-edit-funcionario-print-{page_name}', component_property='children'),

    State(component_id=f'data-table-edit-user-{page_name}',  component_property='data'),
    Input(component_id=f'data-table-edit-user-{page_name}',  component_property='selected_rows'),
    State(component_id=f"mes-ref-{page_name}",  component_property='value'),
    # prevent_initial_callbacks=True,
    )
def editar_turma(data_drom_data_table, list_active_cell, mes_ref):

    if data_drom_data_table and list_active_cell:

        df_turma = pd.DataFrame(data_drom_data_table)

        df_result3 = pd.DataFrame()

        for active_cell in list_active_cell:

            # active_cell = int(active_cell)

            turma_id = df_turma['id'].iloc[active_cell]
            turma_id_dice = df_turma['id_turma'].iloc[active_cell]
            id_turma_dice = int(df_turma['id_turma'].iloc[active_cell])

            # turma_id = df_turma['id'].iloc[active_cell[0]]
            # turma_id_dice = df_turma['id_turma'].iloc[active_cell[0]]
            # id_turma_dice = int(df_turma['id_turma'].iloc[active_cell[0]])

            df_turma2  = dados.query_table(
                table_name='turma_aluno',
                # table_name='turma',
                # field_list=[
                #     {'name': 'email'},
                # ]
                filter_list=[
                    {'op': 'eq', 'name': 'id_turma', 'value': f'{turma_id_dice}'},
                    # {'op': 'eq', 'name': 'id', 'value': f'{turma_id}'},
                ]
            )

            # if len(df_turma2['id_aluno']) >= 1:
            #     print('possui alunos')
            # else:
            #     print('nao possui')
            #     return 'não possui alunos cadastrados'

            list_alunos = df_turma2['id_aluno'].to_list()
            # list_alunos = json.loads(df_turma2['id_aluno'][0])['id_aluno']

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

            for int_month in [mes_ref]:

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

                    # calc frequencia
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
                        1: "1° Sem.",
                        2: "2° Sem.",
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

            df_result3 = pd.concat(
                objs=[df_result3, df_result2],
                ignore_index=True
            )

        columns = [
            {
                "id": i,
                "name": i.replace('_', ' ').upper(),
                # "type": i,
                # "editable": True if hist_columns[i]['editable'] == 1 else False,
                # "presentation": 'dropdown' if i == 'cadastrado' else '',
            } for i in df_result3.columns
        ]

        df_result3['nome'] = df_result3['nome'].apply(
            lambda x: f'{x.split(" ")[0]} {x.split(" ")[1]}' if len(x.split(" ")) > 2 else f'{x.split(" ")[0]}'
        )

        dt_turma = dash_table.DataTable(
            id=f'data-table-hist-aluno-{page_name}',
            data=df_result3.to_dict('records'),
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
            # page_size=30,
            filter_action='native',
            row_selectable="single",
            # sort_mode="multi",
            # sort_action="native",
            # page_action="native",
            editable=False,
            # export_columns='all',
            # export_format='xlsx',
            # editable=False,
            style_header={'textAlign': 'center', 'fontWeight': 'bold'},
            style_as_list_view=True,
            # fixed_columns={'headers': True, 'data': 3},
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

        """
        loop para criar tabelas separadas por pag
        """

        list_tables_print = []
        for turma_id in df_result3['id_turma'].unique():

            # list_columns2 = list_columns.copy()

            # filtrar turma por id
            df_result_x = df_result3[df_result3['id_turma'] == turma_id]

            # stt = df_result_x['status_turma'].unique()[0]
            # removendo
            id_tumma_dice_x = int(df_result_x['id_turma'].unique()[0])
            df_result_x.drop(columns=['id_turma'], inplace=True)

            df_turmax = dados.query_table(
                table_name='turma',
                field_list=[
                    {'name': 'id_professor'},
                    {'name': 'id_coordenador'},
                    {'name': 'status'},
                    {'name': 'escola'},
                ],
                filter_list=[
                    {'op': 'eq', 'name': 'id_turma', 'value': id_tumma_dice_x},
                ]
            )

            id_professor = json.loads(df_turmax['id_professor'][0])
            id_coordenador = json.loads(df_turmax['id_coordenador'][0])
            status = df_turmax['status'].unique()[0]
            escola = df_turmax['escola'].unique()[0]

            df_prof = dados.query_table(
                table_name='funcionario',
            )
            nome_prof = df_prof[df_prof['id'] == id_professor]['nome_completo'].unique()[0]
            nome_coord = df_prof[df_prof['id'] == id_coordenador]['nome_completo'].unique()[0]

            # df_hr_x = dados.query_table(
            #     table_name='turma_horario',
            #     filter_list=[
            #         {'op': 'eq', 'name': 'id_turma', 'value': id_tumma_dice_x},
            #     ]
            # )
            # df_hr_xx = dados.query_table(
            #     table_name='horario',
            #     filter_list=[
            #         {'op': 'in', 'name': 'id', 'value': df_hr_x['id_horario'].to_list()},
            #     ]
            # )

            # df_turma.rename(columns={'status': 'status_turma'}, inplace=True)
            # df_turma.drop(columns=['id_aluno'], inplace=True)



            # if 'id_turma' in list_columns2:
            #     list_columns2.remove('id_turma')
            #     df_result_x.drop(columns=['id_turma'], inplace=True)
            #
            # if 'status_turma' in list_columns2:
            #     list_columns2.remove('id_turma')
            #     df_result_x.drop(columns=['status_turma'], inplace=True)
            #
            # nome_professor = ''
            # if 'nome_professor' in list_columns2:
            #     list_columns2.remove('nome_professor')
            #     nome_professor = df_result_x['nome_professor'].unique()[0]
            #     df_result_x.drop(columns=['nome_professor'], inplace=True)

            # nome_coordenador = ''
            # if 'nome_coordenador' in list_columns2:
            #     list_columns2.remove('nome_coordenador')
            #     nome_coordenador = df_result_x['nome_coordenador'].unique()[0]
            #     df_result_x.drop(columns=['nome_coordenador'], inplace=True)
            #
            # escola = ''
            # if 'escola' in list_columns2:
            #     list_columns2.remove('escola')
            #     escola = df_result_x['escola'].unique()[0]
            #     df_result_x.drop(columns=['escola'], inplace=True)

            escola_info = dbc.Row(
                class_name='pt-2',
                children=[
                    html.H6(
                        children=[
                            f'Prof.: {nome_prof}'.upper()
                        ],
                    ),
                    html.H6(
                        children=[
                            f'Coord.: {nome_coord}'.upper()
                        ],
                    ),
                    html.H6(
                        children=[
                            f'{escola}'.upper()
                        ],
                    ),
                ]
            )

            # linhas horarios
            # rows_horarios = list()
            # for week in list_week_days:
            #
            #     # captura hora da turma
            #     hr_turma = str(df_result_x[f'horario-{week}'].unique()[0])
            #
            #     # validando se coluna está vazia
            #     if hr_turma != 'nan':
            #         """
            #         adiciona horario na linha quando col não for vazia
            #         """
            #         # rows_horarios.append(
            #         #     f"{week} {df_result_x[f'horario-{week}'].unique()[0]}".upper()
            #         # )
            #
            #         rows_horarios.append(
            #             dbc.Row(
            #                 children=[
            #                     dbc.Col(
            #                         class_name='col-4',
            #                         children=[
            #                             f"{week} ".upper()
            #                         ]
            #                     ),
            #                     dbc.Col(
            #                         class_name='col-4',
            #                         children=[
            #                             f"{df_result_x[f'horario-{week}'].unique()[0]}".upper()
            #                         ]
            #                     ),
            #                     dbc.Col(
            #                         class_name='col-10',
            #                     ),
            #                     # f"{week} {df_result_x[f'horario-{week}'].unique()[0]}".upper()
            #                     # f"{week} {df_result_x[f'horario-{week}'].unique()[0]}".upper()
            #                 ],
            #                 # class_name='m-0 p-0'
            #             )
            #         )
            #         rows_horarios.append(html.Br())
            #     # else:
            #
            #     # apagando coluna
            #     df_result_x.drop(columns=[f'horario-{week}'], inplace=True)
            #
            #     # removendo col da lista
            #     list_columns2.remove(f'horario-{week}')

            # criar colunas

            # columns = [
            #     {
            #         "id": all_columns[i]['id'],
            #         "name": all_columns[i]['nome'].replace('_', ' ').upper(),
            #         "type": all_columns[i]['type'],
            #         # "editable": True if filted_columns[i]['type'] == 1 else False,
            #         # "presentation": 'dropdown' if i == 'cadastrado' else '',
            #     } for i in list_columns2
            # ]

            list_tables_print.append(
                dbc.Row(
                    children=[

                        dbc.Row(
                            children=[
                                dbc.Col(
                                    class_name='col-3',
                                    children=[
                                        html.Img(
                                            src="/static/images/logo/logo.webp",
                                            alt='logo',
                                            # className='perfil_avatar mx-auto',
                                            style={'height': '120px', 'width': '270px'},
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    class_name='col-6',
                                    children=[
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    className='col-4',
                                                    children=[
                                                        html.H2(
                                                            children=[
                                                                f'TURMA: {turma_id}',
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                dbc.Col(
                                                    className='col-4',
                                                    children=[
                                                        html.H2(
                                                            children=[
                                                                f'{status}',
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                dbc.Col(
                                                    className='col-4',

                                                ),
                                            ],
                                        ),
                                        # html.H6(
                                        #     children=[
                                        #         f'{status}',
                                        #     ],
                                        # ),
                                        # html.H6(
                                        #     className='pt-2',
                                        #     children=rows_horarios,
                                        # ),
                                    ],
                                ),
                                dbc.Col(
                                    class_name='col-3',
                                    children=escola_info
                                )
                            ],
                        ),

                        dash_table.DataTable(
                            id=f'data-table-hist-aluno-{id_tumma_dice_x}-{page_name}',
                            data=df_result_x.to_dict('records'),
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
                            # page_size=30,
                            # filter_action='native',
                            # sort_mode="multi",
                            # sort_action="native",
                            page_action="native",
                            # export_columns='all',
                            # export_format='xlsx',
                            editable=False,
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

                        ),

                        html.P('')

                    ],
                    class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0'
                )
            )

        # saida para inpressao
        output_print = dbc.Row(
            id=f'row-print-{page_name}',
            children=list_tables_print,
            className='p-0 m-0',
        )


        datatable1 = dbc.Row(
            children=[
                dt_turma,
                # output_print

            ],
            class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 overflow-auto'
        )
        # datatable1 = dbc.Row(dt_user, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    else:

        dt_func = dash_table.DataTable(id=f'data-table-edit-func-{page_name}',)

        datatable1 = dbc.Row(dt_func, class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 overflow-auto')

        output_print = ''

    # caputra mes ref STR
    meses_ref = {
        1: "Mar/Abr",
        2: "Mai/Jun",
        3: "Ago/Set",
        4: "Out/Nov",
    }

    month_ref = f'NOTA'

    return datatable1, '', month_ref
    # return datatable1, '', month_ref if active_cell else ""



@callback(
    Output(component_id=f'out-edit-funcionario-print-{page_name}', component_property='children'),
    Output(component_id=f"output-alunos-{page_name}", component_property='children'),
    Output(component_id=f'out-alert-imp-aluno-{page_name}', component_property='children'),

    State(component_id=f'inp-turma-load-{page_name}',  component_property='value'),
    Input(component_id=f"mes-ref-{page_name}", component_property='value'),
    Input(component_id=f'inp-alunos-load-{page_name}', component_property='value'),
    prevent_initial_callbacks=True,
    )
def gerar_out_print(
        id_turma,
        mes_ref,
        id_aluno,
):
    semestre = mes_ref

    meses_ref = {
        1: [1, 2],
        2: [3, 4],
    }

    mes_ref = meses_ref[mes_ref]

    if id_aluno:

        turma_id_dice = int(id_turma)
        id_aluno = int(id_aluno)


        df_all_aluno  = dados.query_table(
            table_name='aluno',
            # field_list=[
            #     {'name': 'email'},
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': id_aluno},
            ]
        )

        df_all_aluno.rename(columns={'id': 'id_aluno'}, inplace=True)

        df_result = pd.DataFrame(
            data={
                'id_aluno': df_all_aluno['id_aluno'],
                'nome': df_all_aluno['nome'],
            }
        )

        df_hist_turma  = dados.query_table(
            table_name='historico_aluno',
            # field_list=[
            #     {'name': 'email'},
            # ]
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': int(turma_id_dice)},
                {'op': 'in', 'name': 'mes_ref', 'value': mes_ref},
                # {'op': 'eq', 'name': 'mes_ref', 'value': int(int_month)},
                {'op': 'eq', 'name': 'id_aluno', 'value': int(id_aluno)},
            ]
        )

        df_t_horas = dados.query_table(
            table_name='turma_horario',
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': int(turma_id_dice)},
            ]
        )
        df_horas = pd.DataFrame()
        if not df_t_horas.empty:
            df_horas = dados.query_table(
                table_name='horario',
                filter_list=[
                    {'op': 'in', 'name': 'id', 'value': df_t_horas['id_horario'].to_list()},
                ]
            )


        df_merge = pd.merge(
            left=df_all_aluno,
            right=df_hist_turma,
            how='left',
            on=['id_aluno'],
        )
        df_merge['id_turma'] = turma_id_dice

        df_turma = dados.query_table(
            table_name='turma',
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': int(turma_id_dice)},
                # {'op': 'in', 'name': 'mes_ref', 'value': mes_ref},
                # {'op': 'eq', 'name': 'mes_ref', 'value': int(int_month)},
                # {'op': 'eq', 'name': 'id_aluno', 'value': int(id_aluno)},
            ]
        )

        id_professor = json.loads(df_turma['id_professor'][0])
        id_coordenador = json.loads(df_turma['id_coordenador'][0])
        escola = df_turma['escola'][0]

        df_prof = dados.query_table(
            table_name='funcionario',
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': int(id_professor)},
            ]
        )

        df_coord = dados.query_table(
            table_name='funcionario',
            filter_list=[
                {'op': 'eq', 'name': 'id', 'value': int(id_coordenador)},
            ]
        )

        year = df_turma['inicio'][0].year
        nome_prof = df_prof['nome_completo'][0]
        nome_coord = df_coord['nome_completo'][0]

        # calc frequencia
        df_merge['frequency_pct'] = 1 - (df_merge['numero_faltas'] / df_merge['numero_aulas'])
        df_merge['frequency'] = df_merge['frequency_pct'] * 10
        df_merge['frequency_pct'] = df_merge['frequency_pct'] * 100

        df_merge['frequency_pct'] = df_merge['frequency_pct'].apply(
            lambda x: f'{x} %',
        )

        materias = [
            'frequency',
            'research',
            'organization',
            'interest',
            'group_activity',
            'speaking',
            'frequencia_of',
            'listening',
            'readind_inter',
            'writing_process',
        ]

        notas = []
        for idx, row in df_merge.iterrows():
            # print(f'- {row["id_aluno"]}')

            aux = 0
            for mm in materias:
                aux = aux + row[mm]

            notas.append(
                round(
                    (aux / len(materias)),
                    2
                )
            )

        # month_str = meses_ref[int_month]
        df_merge[f'media'] = notas

        for m in materias:
            df_result[m] = df_merge[m]


        """
        fim for
        """

        """
        ordenando tabela
        """


        df_merge[['mes_ref'] + materias].columns

        rename = {
            'mes_ref': 'mes_ref',
            'frequency': '01) Frequency:',
            'research': '02) Research: Home Tasks',
            'organization': '03) Organization: Indiv./ Group. Orders. Commands and Rules',
            'interest': '04) Interest in English Language',
            'group_activity': '05) Group Activity',
            'speaking': '06) Speaking and Locution:',
            'frequencia_of': '07) Frequency of Native Language Interferance',
            'listening': '08) Listening Comprehesion',
            'readind_inter': '09) Readind Tnterpretation',
            'writing_process': '10) Writing Process',
            'media': 'Bimonth Average',
            }


        df_merge.rename(columns=rename,inplace=True)

        df_pivot = df_merge[
            [rename[x] for x in rename]
        ].pivot_table(
            values=[rename[x] for x in rename],
            columns=[
                rename['mes_ref'],
            ]
        ).reset_index().rename(
            columns={
                "index": "aspects_evaluated"
            }
        )

        # criando sempre  bim 1 e 2
        for idx, x in enumerate(mes_ref):
            df_pivot[idx + 1] = df_pivot[x]

            # convert date
        df_merge['age'] = df_merge['dat_nasc'].astype(str).apply(CalculateAge)

        sem_avg = f"Semester Average"

        df_row_avg = pd.DataFrame(
            data={
                'aspects_evaluated': [
                    sem_avg,
                    # f"(Bim 1 + Bim 2) / 2"
                ],
                1: [
                    df_merge['Bimonth Average'].mean()
                ],
            }
        )

        df_pivot = pd.concat(objs=[df_pivot, df_row_avg], ignore_index=True)

        columnDefs = [
            {
                "field": 'aspects_evaluated',
                "headerName": 'ASPECTS EVALUATED',
                # 'suppressSizeToFit': True,
                'editable': False,
                "sortable": False,
                'pinned': 'left',
                'width': 660,
            },
             {
                 "field": '1',
                 "headerName": 'Bimonth 1',
                 # 'suppressSizeToFit': True,
                 'editable': False,
                 "sortable": False,
                 'width': 100,
                 # "type": "numericColumn",
                 # "columnTypes": "centerAligned",
                 "cellStyle": {
                     'textAlign': 'center',
                 },
                 # 'headerClass': 'center-aligned-group-header',
             },
             {
                 "field": '2',
                 "headerName": 'Bimonth 2',
                 # 'suppressSizeToFit': True,
                 'editable': False,
                 "sortable": False,
                 'width': 100,
                 # "type": "numericColumn",
                 # "columnTypes": "centerAligned",
                 "cellStyle": {
                     'textAlign': 'center',
                 },
                 # 'headerClass': 'center-aligned-group-header',
             },
        ]

        rowClassRules = {
            "fw-bold fs-6": "params.data.aspects_evaluated == 'Bimonth Average'",
            "fw-bold fs-5": "params.data.aspects_evaluated == '{}'".format(sem_avg),
        }

        body_content = [
            dbc.Row(
                class_name='px-2',
                children=[
                    dag.AgGrid(
                        id=f'data-table-boletim-aluno-{page_name}',
                        columnDefs=columnDefs,
                        rowData=df_pivot.to_dict('records'),
                        dashGridOptions={
                            "animateRows": True,
                            "domLayout": 'print',
                            'sortable': False,
                            'dataTypeDefinitions': {
                                "number": {
                                    "baseDataType": "number",
                                    "extendsDataType": "number",
                                    "columnTypes": "centerAligned",
                                    "appendColumnTypes": True
                                },
                            }
                        },
                        rowClassRules=rowClassRules,
                        columnSize="sizeToFit",
                        # style={"height": 600, "width": 400}
                    )
                ]
            ),
        ]



        col2 = dbc.Row(
            children=[
                dbc.Row(
                    class_name='comments-size',
                    children=[
                        dbc.Row(
                            children=[
                                x,
                                html.Br(),
                                html.Br(),
                            ]
                        )
                        for x in df_merge['descricao'].to_list()
                    ]
                ),
                dbc.Row(
                    class_name='fw-bold ',
                    children=[
                        nome_prof
                    ]
                ),
            ]
        )

        col1 = dbc.Row(
            children=[

                # HEADER
                dbc.Row(
                    className='pb-5 pt-3 mx-1',
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('NAME'), ], className='col-3'),
                                        dbc.Col(children=[df_merge['nome'].unique()[0]], className='col-9'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('AGE'), ], className='col-3'),
                                        dbc.Col(children=[df_merge['age'].unique()[0]], className='col-9'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('TEACHER'), ], className='col-3'),
                                        dbc.Col(children=[nome_prof], className='col-9'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('COORDINATOR'), ], className='col-3'),
                                        dbc.Col(children=[nome_coord], className='col-9'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('SEMESTER'), ], className='col-3'),
                                        dbc.Col(children=[semestre], className='col-9'),
                                    ]
                                ),
                            ],
                            class_name='col-6'
                        ),
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B(''), ], className='col-4'),
                                        dbc.Col(children=[], className='col-8'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('START STUDYING'), ], className='col-4'),
                                        dbc.Col(children=[f"{df_merge['inicio'].unique()[0]:%Y-%m-%d}"], className='col-8'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('TEACHER'), ], className='col-4'),
                                        dbc.Col(children=[nome_prof], className='col-8'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('ABSCENCES'), ], className='col-4'),
                                        dbc.Col(children=[int(df_merge['numero_faltas'].sum())], className='col-8'),
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(children=[html.B('YEAR'), ], className='col-4'),
                                        dbc.Col(children=[year], className='col-8'),
                                    ]
                                ),
                            ],
                            class_name='col-6'
                        ),
                    ],
                ),
                dbc.Row(
                    class_name='',
                    children=[
                        dbc.Row(children=body_content),
                    ]
                )
            ],
        )

        scd_pag = dbc.Row(
            children=[
                dbc.Row(
                    class_name='pt-4',
                    children=[
                        dbc.Col(
                            class_name='col-6 ',
                            children=[
                                dbc.Row(
                                    className='',
                                    children=[
                                        html.Img(
                                            src="/static/images/logo/logo.webp",
                                            alt='logo',
                                            # className='perfil_avatar mx-auto',
                                            style={'height': '150x', 'width': '350px'},
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dbc.Col(
                            class_name='col-6 pt-5 mt-5 col',
                            children=[
                                dbc.Row(
                                    class_name='center-aligned-group-header pb-2',
                                    children=[
                                        html.H3(children=['COMMENTS']),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),


                dbc.Col(
                    children=[
                      col1
                    ],className='col-6 tamanho-letra',
                    # style={"border":"2px black solid"}
                ),
                dbc.Col(
                    children=[
                      col2
                    ],className='col-6 px-5',
                    # style={"border":"2px black solid"}
                ),
            ]
        )

        columnDefs3 = [
            {
                "field": 'branch',
                "headerName": f'BRANCH: {escola}'.upper(),
                'editable': False,
                "sortable": False,
                # 'width': 100,
                'children' : [
                    {
                        "field": 'days',
                        "headerName": f'DAYS  SCHEDULE',
                        'editable': False,
                        "sortable": False,
                        'width': 310,
                    },
                    {
                        "field": 'from',
                        "headerName": f'',
                        'editable': False,
                        "sortable": False,
                        'width': 100,
                        # "cellClass": "bg-secondary bg-gradient bg-opacity-50",
                        'cellClassRules': {
                            "fw-bold": "params.data.from == 'FROM' ",
                            # "fw-bold fs-6": "params.data.from == 'FROM'",
                            # 'text-warning text-center fs-4': '5 <= params.value &&  params.value < 8  ',
                            # 'text-success text-start fs-6': 'params.value < 5',
                        },
                    },
                    {
                        "field": 'inicio',
                        "headerName": f'',
                        'editable': False,
                        "sortable": False,
                        'width': 100,
                    },
                    {
                        "field": 'up_to',
                        "headerName": f'',
                        'editable': False,
                        "sortable": False,
                        'width': 100,
                        'cellClassRules': {
                            "fw-bold": "params.data.up_to == 'UP TO' ",
                            # "fw-bold fs-6": "params.data.from == 'FROM'",
                            # 'text-warning text-center fs-4': '5 <= params.value &&  params.value < 8  ',
                            # 'text-success text-start fs-6': 'params.value < 5',
                        },
                    },
                    {
                        "field": 'fim',
                        "headerName": f'',
                        'editable': False,
                        "sortable": False,
                        'width': 250,
                    },
                ],
            },
        ]
        rowClassRules2 = {
            # "fw-bold fs-6": "params.data.from == 'FROM'",
            # 'font-weight-bold': 'FROM = params.data.from && UP TO = params.data.up_to',
        }

        if not df_horas.empty:
            df_header2 = pd.DataFrame(
                data={
                    'days': df_horas['dia_semana'].to_list(),
                    'from': [ "FROM" for x in df_horas['dia_semana'].to_list()],
                    'inicio': [
                        f"{str(row['hora_inicio']).zfill(2)}:{str(row['min_inicio']).zfill(2)}"
                        for idx, row in df_horas.iterrows()
                    ],
                    'up_to': [ "UP TO" for x in df_horas['dia_semana'].to_list()],
                    'fim': [
                        f"{str(row['hora_fim']).zfill(2)}:{str(row['min_fim']).zfill(2)}"
                        for idx, row in df_horas.iterrows()
                    ],
                }
            )

            ag_h_2 = dag.AgGrid(
            id=f'data-table-header-2-{page_name}',
            columnDefs=columnDefs3,
            rowData=df_header2.to_dict('records'),
            dashGridOptions={
                "animateRows": True,
                "domLayout": 'print',
                'sortable': False,
                # 'groupHeaderHeight': 50,
                'headerHeight': 50,
                # 'floatingFiltersHeight': 40,
            },
            rowClassRules=rowClassRules2,
            columnSize="sizeToFit",
            # style={"height": 600, "width": 400}
        )

        ag_h_3 = dbc.Row(
            class_name='col-11',
            children=[
                dbc.Col(
                    class_name='col-4 text-center',
                    children=[
                        dbc.Row(
                            children=[
                                html.H6(children=['Teacher'.title()])
                            ],
                        ),
                        html.Br(),
                        html.Hr(),
                    ],
                ),
                dbc.Col(
                    class_name='col-4 text-center',
                    children=[
                        dbc.Row(
                            children=[
                                html.H6(children=['Coordnator'.title()])
                            ],
                        ),
                        html.Br(),
                        html.Hr(),
                    ],
                ),
                dbc.Col(
                    class_name='col-4 text-center',
                    children=[
                        dbc.Row(
                            children=[
                                html.H6(children=['Principal'.title()])
                            ],
                        ),
                        html.Br(),
                        html.Hr(),
                    ],
                ),
            ],
        )
        columnDefs4 = [
            {
                # "field": 'dice',
                "headerName": 'DICE ENGLISH COURSE',
                # 'suppressSizeToFit': True,
                'editable': False,
                "sortable": False,
                'pinned': 'left',
                # 'width': 860,
                'children': [
                    {
                        # "field": 'end',
                        "headerName": 'R Fonte da Saudade, 193 - Lagoa - Teles - 3215-2380 / 98182-8785',
                        # 'suppressSizeToFit': True,
                        'editable': False,
                        "sortable": False,
                        'pinned': 'left',
                        # 'width': 860,
                        'children': [
                            {
                                "field": 'email',
                                "headerName": 'emai'.upper(),
                                # 'suppressSizeToFit': True,
                                'editable': False,
                                "sortable": False,
                                'pinned': 'left',
                                'width': 430,
                            },
                            {
                                "field": 'site',
                                "headerName": 'site'.upper(),
                                # 'suppressSizeToFit': True,
                                'editable': False,
                                "sortable": False,
                                'pinned': 'left',
                                'width': 430,
                            },

                        ]
                    },

                ]
            },
        ]

        rowClassRules4 = {
            "fw-bold fs-6": "params.data.email == 'dice@dice.com.br'",
        }

        df_h4 = pd.DataFrame(
            data={
                'email': ['dice@dice.com.br'],
                'site': ['www.dice.com.br'],
            }
        )

        ag_h_4 = dag.AgGrid(
            id=f'data-table-ag-4-{page_name}',
            columnDefs=columnDefs4,
            rowData=df_h4.to_dict('records'),
            dashGridOptions={
                "animateRows": True,
                # "domLayout": 'autoHeight',
                "domLayout": 'print',
                'sortable': False,
                # "headerClass": 'center-aligned-header',
                "headerClass": 'center-aligned-group-header',
                'headerHeight': 50,
            },
            rowClassRules=rowClassRules4,
            columnSize="sizeToFit",
            style={"height": 200}
        )

        header2 = dbc.Row(
            children=[
                dbc.Row(
                    class_name='pb-2',
                    children=[
                        html.H2(children=['TIMETABLE DURING THIS SEMESTER'.title()])
                    ],
                ),
                dbc.Row(
                    class_name='header2',
                    children=[
                        ag_h_2
                    ],
                ),
                dbc.Row(
                    children=[
                        html.Br()
                        for x in range(0,  24-len(df_header2['days']))
                    ]
                ),
                dbc.Row(
                    children=[
                        ag_h_3
                    ]
                ),
                dbc.Row(
                    class_name='header3',
                    children=[
                        ag_h_4
                    ]
                ),

            ],
        )

        path_file = f'static/images/aluno/{df_merge["foto"][0]}'
        path_no_foto = f'static/images/logo/no_foto.png'
        foto_user = path_file if os.path.isfile(path_file) else path_no_foto

        columnDefs5 = [
            {
                "field": 'tt',
                "headerName": f'',
                'editable': False,
                "sortable": False,
                'width': 150,
                'cellStyle': {
                    # 'background-color': '#66c2a5',
                    'font-weight': 'bold',
                }
            },
            {
                "field": 'bb',
                "headerName": f'',
                'editable': False,
                "sortable": False,
                'width': 710,
            },
        ]

        df_5 = pd.DataFrame(
            data={
                'tt': [
                    'PERÍOD:',
                    'TEACHER',
                    'COORD.:',
                    'PRINCIPAL',
                ],
                'bb': [
                    f'{year} - {semestre}ST SEMESTER',
                    f'{nome_prof}'.upper(),
                    f'{nome_coord}'.upper(),
                    'MARIA ESTHER L. PRATES',
                ],
            }
        )


        ag_5 = dag.AgGrid(
            id=f'data-table-ag-5-{page_name}',
            columnDefs=columnDefs5,
            rowData=df_5.to_dict('records'),
            dashGridOptions={
                "animateRows": True,
                "domLayout": 'print',
                'sortable': False,
                'headerHeight': 50,
            },
            # rowClassRules=rowClassRules5,
            columnSize="sizeToFit",
        )

        col4 = dbc.Row(
            children=[
                dbc.Row(
                    class_name='center-aligned-group-header pb-2 px-5',
                    children=[
                        dbc.Col(
                            class_name='col-8',
                            children=[
                                html.Img(
                                    src="/static/images/logo/logo.webp",
                                    alt='logo',
                                    style={
                                        'height': '240px',
                                        # 'width': '540'
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                dbc.Row(
                    class_name='pt-1',
                    children=[
                        html.Br(),
                    ],
                ),
                dbc.Row(
                    class_name='center-aligned-group-header',
                    children=[
                        html.H2(children=['STUDENTS REPORT CARD']),
                    ],
                ),

                dbc.Row(
                    class_name='pt-1',
                    children=[
                    ],
                ),
                dbc.Row(
                    children=[
                        html.Img(
                            id=f'img-user-{page_name}',
                            src=foto_user,
                            alt=f"ALUNO {df_merge['nome'].unique()[0]}".upper(),
                            # style={
                            #     'height': '450px',
                            #     'width': '450px',
                            # },
                            className='img-logo2',
                        ),
                    ],
                    class_name='px-0 justify-content-center pb-2 pt-2'
                ),
                dbc.Row(
                    class_name='center-aligned-group-header pt-4',
                    children=[
                        html.H4(children=[
                            f"{df_merge['nome'].unique()[0]}"
                        ],
                        )
                    ],
                ),
                dbc.Row(
                    class_name='pt-5',
                    children=[
                    ],
                ),
                dbc.Row(
                    class_name='pt-4',
                    children=[
                        ag_5,
                    ],
                ),
            ],
        )



        fst_pag = dbc.Row(
            children=[

                dbc.Col(
                    children=[
                      header2
                    ],className='col-6 tamanho-letra',
                    # style={"border":"2px black solid"}
                ),
                dbc.Col(
                    children=[
                      col4
                    ],className='col-6 px-5',
                    # style={"border":"2px black solid"}
                ),
            ]
        )


        datatable1 = dbc.Row(
            id=f'row-print-{page_name}',
            children=[
                fst_pag,
                html.P(),
                scd_pag,
            ],
            className='px-4 m-0 pt-5',
        )

        output_alert = f''
    else:


        datatable1 = dbc.Row(
            children=[],
            # class_name='col-lg-12 col-md-12 col-sm-12 p-0 m-0 overflow-auto'
        )

        output_alert = f'2'

    return datatable1, datatable1, output_alert