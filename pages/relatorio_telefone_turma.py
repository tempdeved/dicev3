import glob
import os.path

import dash
import pandas as pd

import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo

from banco.dados import Dados
from config.config import Config

from string import Template

from utils.get_idade import CalculateAge
from utils.create_excel import Turma_xlsx

# page_name = __name__[6:].replace('.', '_')
page_name='RelatorioTelefoneTurma'
dash.register_page(__name__, path=f'/{page_name}')

config = Config().config
dados = Dados(config['ambiente'])
cfg_relatorio_simples = config['relatorio_telefone_turma']

content_layout = dbc.Row(
    id=f'main-container-{page_name}',
    class_name='px-2 mx-0 shadow-lg',
    children=[

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

                                            # retorno vazio da funcao JS de imprimpri
                                            dbc.Row(id=f"notification-output-{page_name}"),

                                            dbc.Row(
                                                class_name='pb-3',
                                                children=[
                                                    dbc.Select(
                                                        id=f"tabela-options-{page_name}",
                                                        options=[
                                                            # {"label": "Somente alunos", "value": '1'},
                                                            {"label": "Turmas", "value": '2'},
                                                        ],
                                                        value='2',
                                                        # inline=True,
                                                    ),
                                                ]
                                            ),

                                            dbc.Row(
                                                children=[
                                                    dbc.Accordion(
                                                        children=[
                                                            dbc.AccordionItem(
                                                                children=[

                                                                    dbc.Row(
                                                                        class_name='py-3',
                                                                        children=[

                                                                            dbc.Row(
                                                                                id=f'out-check-box-columns-{page_name}',
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                                className='m-0 p-0',
                                                                # style={'background-color': '#ffffff'},
                                                                title="FILTRO",
                                                            ),
                                                        ],
                                                        className='m-0 p-0',
                                                        start_collapsed=True,
                                                        flush=True,
                                                        # style={'background-color': '#ffffff'}
                                                    )
                                                ],
                                                className='m-0 p-1',
                                            ),

                                            dbc.Row(
                                                id=f'button-area-{page_name}',
                                                class_name='ml-0 pt-2',  # gap-2
                                                children=[
                                                    dbc.Col(
                                                        # width=2,
                                                        children=[
                                                            dbc.Button(
                                                                id=f'btn-buscar-generico-{page_name}',
                                                                children=['BUSCAR'],
                                                                class_name='me-0',
                                                                color='primary',
                                                                n_clicks=0,
                                                            ),
                                                        ]
                                                    ),

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
                                                            dbc.Button(
                                                                id=f'btn-download-turma-{page_name}',
                                                                children=['DOWNLOAD /TURMA'],
                                                                class_name='me-0',
                                                                color='primary',
                                                                n_clicks=0,
                                                            ),
                                                            dcc.Download(id=f"out-download-turma-{page_name}")
                                                        ]
                                                    ),
                                                ]
                                            ),

                                            dbc.Tabs(
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
                                                    ],
                                                    label='Resultado'
                                                )
                                            ),


                                            # dbc.Row(id=f'out-edit-func-{page_name}'),

                                        ],
                                        style={'background-color': '#ffffff'},
                                        title="Relatório Telefones P/ Turma"
                                    )
                                ], start_collapsed=False, flush=True, style={'background-color': '#ffffff'}
                            ),
                        ], class_name=''
                    )
                ]
            ),
        # dbc.Alert(
        #     children=[
        #         dbc.Row(id=f'out-alert-user-{page_name}'),
        #         dbc.Row(id=f'out-alert-fuc-{page_name}'),
        #         dbc.Row(id=f'out-alert-edited-fuc-{page_name}'),
        #     ]
        # )
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


print_page = f'data-table-edit-user-{page_name}'


js_model_print = Template("""
function (n_clicks) {
        var page =  '$print_page'
        var n = n_clicks
        console.log('n')
        console.log(n)
        console.log('n_clicks')
        console.log(n_clicks)
        console.log(n + '- TESTE-----')
        
        const content = document.getElementById(page).innerHTML;
        const printWindow = window.open('', '_blank');
        printWindow.document.write('<html>');
        
        printWindow.document.write('<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/zephyr/bootstrap.min.css\">');
        printWindow.document.write('<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap-grid.min.css\">');
        printWindow.document.write('<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css\">');

        printWindow.document.write('<head><title>Print</title></head><body>');
            
        printWindow.document.write(content);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
  
        console.log(page)
        
        return ''
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
    Output(component_id=f"out-download-turma-{page_name}", component_property="data"),
    State(component_id=f'data-table-edit-user-{page_name}', component_property="data"),
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
    Output(component_id=f'out-check-box-columns-{page_name}', component_property='children'),

    Input(component_id=f"tabela-options-{page_name}", component_property='value'),
)
def filter_columns(table_radio):
    # check_box = f'table_radio={table_radio}'

    table_radio = int(table_radio)

    # table_name = cfg_relatorio_simples['radio_itens'][table_radio]['table_name']
    filted_columns = cfg_relatorio_simples['radio_itens'][table_radio]['filted_columns']
    default_columns = cfg_relatorio_simples['radio_itens'][table_radio]['default_columns']
    # columns = cfg_relatorio_simples['radio_itens'][table_radio]['columns']

    opt = []

    for x in filted_columns:
        if filted_columns[x]['ckbox'] == True:
            b = {
                "label": x.replace('_', ' ').title(),
                "value": x
            }
            opt.append(b)

    if table_radio == 1:

        check_box = dbc.Checklist(
            options=opt,
            value=default_columns,
            id=f"check-columns-{page_name}",
            inline=True,

        )
    elif table_radio == 2:
        check_box = dbc.Checklist(
            options=opt,
            value=default_columns,
            id=f"check-columns-{page_name}",
            inline=True,

        )

    return check_box

@callback(
    Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),

    # Input(component_id=f'main-container-{page_name}', component_property='children'),
    State(component_id=f"tabela-options-{page_name}", component_property='value'),
    State(component_id=f"check-columns-{page_name}", component_property='value'),
    Input(component_id=f'btn-buscar-generico-{page_name}', component_property='n_clicks'),
)
def capturar_alunos(table_radio, check_box_columns, btn_buscar):


    table_radio = int(table_radio)

    table_name = cfg_relatorio_simples['radio_itens'][table_radio]['table_name']
    filted_columns = cfg_relatorio_simples['radio_itens'][table_radio]['filted_columns']
    # default_columns = cfg_relatorio_simples['radio_itens'][table_radio]['default_columns']
    # columns = cfg_relatorio_simples['radio_itens'][table_radio]['columns']


    if table_radio == 1:

        # query
        df_bruto = dados.query_table(table_name=table_name)

        # recebendo colunas filtradas
        list_columns = check_box_columns

        # df_bruto['bairro'] = 'bairro'
        # df_bruto['cidade'] = 'cidade'
        # df_bruto['uf'] = 'uf'
        # df_bruto['cep'] = 'cep'

        # resebendo resultado
        df_result = df_bruto[['nome']]
        df_result['endereco'] = df_bruto['endereco']
        df_result['bairro/cidade'] = df_bruto['bairro'] +' - '+ df_bruto['cidade']
        df_result['uf/cep'] = df_bruto['uf'] +' - '+ df_bruto['cep']

    elif table_radio == 2:

        list_columns = check_box_columns

        # query
        weekday = ['SEGUNDA-FEIRA']
        status_turma = 'ATIVA'

        # captura horarios
        df_horario  = dados.query_table(table_name='horario',)
        df_horario.rename(columns={'id': 'id_horario'}, inplace=True)

        # captura horarios de turmas
        df_turma_horario  = dados.query_table(table_name='turma_horario',)
        df_turma_horario.drop(columns=['id'], inplace=True)

        # captura turmas
        df_turma_aluno = dados.query_table(table_name=table_name)
        df_turma_aluno.drop(columns=['id'], inplace=True)

        # captura alunos
        df_aluno  = dados.query_table(table_name='aluno',)

        # rename aluno
        df_aluno.rename(
            columns={
                'id': 'id_aluno',
                'status': 'status_aluno',
                'inicio': 'inicio_aluno',
            },
            inplace=True
        )

        # filtrar dia da semana
        df_horario_filted = df_horario[df_horario['dia_semana'].isin(weekday)]
        df_horario_filted.rename(columns={'id':'id_horario'}, inplace=True)
        list_week_ids = df_horario_filted['id_horario'].unique()

        # captura turmas e seu dia da semana filtrado
        df_merge_horarios = pd.merge(
            left=df_turma_horario[df_turma_horario['id_horario'].isin(list_week_ids)],
            right=df_horario_filted,
            how='left',
            on=['id_horario'],
        )

        list_turmas_ids = []
        for x in df_merge_horarios['id_turma'].unique():
            list_turmas_ids.append(int(x))

        df_turma = dados.query_table(
            table_name='turma',
            filter_list=[
                {'op': 'in', 'name': 'id_turma', 'value': list_turmas_ids},
                {'op': 'eq', 'name': 'status', 'value': status_turma},
            ]
        )
        df_turma.rename(columns={'status': 'status_turma'}, inplace=True)
        df_turma.drop(columns=['id_aluno'], inplace=True)

        # merge alunos e turmas
        df_merge_aluno = pd.merge(
            left=df_turma,
            right=df_turma_aluno,
            how='left',
            on=['id_turma']
        )


        # merge alunos detalhes
        df_merge_aluno2 = pd.merge(
            left=df_merge_aluno,
            right=df_aluno,
            how='left',
            on=['id_aluno']
        )

        # ff = [
        #     'id_turma', 'status_turma', 'id_aluno', 'status_aluno', 'nome', 'dat_nasc', 'telefone1', 'responsavel_financeiro',
        #     'tel_responsavel_financeiro'
        # ]

        # df_merge_aluno3 = df_merge_aluno2[ff]
        df_merge_aluno3 = df_merge_aluno2



        """
        capturando Turmas e Horarios
        """

        # merge horarios
        df_merge_turma = pd.merge(
            left=df_turma,
            right=df_turma_horario,
            how='left',
            on=['id_turma']
        )

        # merge detalhe horarios
        df_merge_turma2 = pd.merge(
            left=df_merge_turma,
            right=df_horario,
            how='left',
            on=['id_horario']
        )
        # ff = [
        #     'id_turma', 'status_turma', 'nivel', 'inicio', 'fim', 'dia_semana',
        #     'hora_inicio', 'min_inicio', 'hora_fim', 'min_fim',
        # ]

        # df_merge_turma2 = df_merge_turma2[ff]
        df_merge_turma2 = df_merge_turma2

        # concat 'horario'
        df_merge_turma2['horario'] = df_merge_turma2['hora_inicio'].str.zfill(2) + ':' + df_merge_turma2['min_inicio'].str.zfill(2) + ' - ' + df_merge_turma2['hora_fim'].str.zfill(2) + ':' + df_merge_turma2['min_fim'].str.zfill(2)

        df_pivot1 = pd.pivot(
            data=df_merge_turma2,
            columns=['dia_semana',],
            index=['id_turma'],
        )


        df_pivot2 = df_pivot1.reset_index(level=0)


        """
        MERGE Turma Aluno / Turma Horario
        """






        list_r_name = []

        for x in df_pivot2.columns:
            a = x[0] + '-' +x[1]
            list_r_name.append(a)

        # drop level to merge
        df_pivot3 = df_pivot2.droplevel(level=1, axis=1)

        # renomeando pela ordem das colunas
        df_pivot4 = df_pivot3.set_axis(list_r_name, axis=1)
        df_pivot4.rename(columns={'id_turma-':'id_turma'}, inplace=True)


        list_week_days = df_merge_turma2['dia_semana'].unique()
        list_week_days1 = ['id_turma']

        for x in list_week_days:
            a = 'horario-' + x
            list_week_days1.append(a)


        df_merge_4 = pd.merge(
            left=df_merge_aluno3,
            right=df_pivot4[list_week_days1],
            how='left',
            on=['id_turma']
        )

        #convert date

        df_merge_4['idade'] = df_merge_4['dat_nasc'].astype(str).apply(CalculateAge)



        # cc = ['id_turma', 'status_turma', 'id_aluno', 'status_aluno', 'nome',
        #        'dat_nasc', 'idade', 'telefone1', 'responsavel_financeiro',
        #        'tel_responsavel_financeiro', 'horario-SEGUNDA-FEIRA',
        #        'horario-QUARTA-FEIRA']

        # df_result = df_merge_4

        # remove id_turma to append horarios
        list_week_days1.remove('id_turma')
        list_columns = list_columns + list_week_days1

        df_result = df_merge_4[list_columns]

        # path_folder = 'download'
        # filename = page_name + '.xlsx'
        # file_path = os.path.join(path_folder, filename)
        #
        # # create file
        # Turma_xlsx(file_path=file_path, df=df_result)
        #
        # with pd.ExcelWriter(file_path) as writer:
        #
        #     for idx, turma in enumerate(df_result['id_turma'].unique()):
        #         df_result[df_result['id_turma'] == turma].to_excel(
        #             writer, sheet_name=f"{idx + 1}-{turma}",
        #             index=False,
        #         )

    # DASH DATA TABLE
    dt = dash_table.DataTable(
        id=f'data-table-edit-user-{page_name}',
        # filtrando data frame
        data=df_result[list_columns].to_dict('records'),
        columns=[
            {
                "id": filted_columns[i]['id'],
                "name": filted_columns[i]['nome'].replace('_', ' ').upper(),
                "type": filted_columns[i]['type'],
                # "editable": True if filted_columns[i]['type'] == 1 else False,
                # "presentation": 'dropdown' if i == 'cadastrado' else '',
            } for i in list_columns
        ],
        # page_current=0,
        # page_size=30,
        # style_cell={'textAlign': 'center'},
        editable=False,
        # content_style='grow',
        # filter_action='native',
        # sort_mode="multi",
        # sort_action="native",
        page_action="native",
        # row_selectable="single",
        export_columns='all',
        export_format='xlsx',
        # row_selectable="multi",
        style_header={'textAlign': 'left', 'fontWeight': 'bold'},
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': col},
                'textAlign': 'left'
            } for col in [check_box_columns]
        ],
        # style_data_conditional=[
        #     {
        #         'if': {
        #             'filter_query': '{{Temperature}} = {}'.format(df['Temperature'].min()),
        #         },
        #         'backgroundColor': '#FF4136',
        #         'color': 'white'
        #     },
        # ]

    )
    datatable1 = dbc.Row(dt, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    return datatable1
