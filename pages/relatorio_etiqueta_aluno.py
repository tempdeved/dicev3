import glob
import os.path
from datetime import datetime, date

import dash
import pandas as pd

import dependecies
from dash import html, dcc, dash_table, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc

from flask import Flask, request, redirect, session, url_for
from flask_login import current_user

from elements.titulo import Titulo
from elements.check_list import CheckList
from elements.dropdown import DropDownMenu

from banco.dados import Dados
from config.config import Config

from string import Template

from utils.get_idade import CalculateAge
from utils.create_excel import Turma_xlsx

# page_name = __name__[6:].replace('.', '_')
page_name='RelatorioEtiquetaAluno'
dash.register_page(__name__, path=f'/{page_name}')

config = Config().config
dados = Dados(config['ambiente'])
cfg_relatorio_simples = config['relatorio_etiqueta_alunos']

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
                                                                children=['DOWNLOAD P/ TURMA'],
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
                                                    ],
                                                    label='Resultado'
                                                )
                                            ),


                                            # dbc.Row(id=f'out-edit-func-{page_name}'),

                                        ],
                                        style={'background-color': '#ffffff'},
                                        title="Relatório Etiquetas"
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


# print_page = f'data-table-edit-user-{page_name}'
# print_page = f'row-print-{page_name}'
print_page = f'out-edit-funcionario-print-{page_name}'
# print_page = f'collapse-print-{page_name}'


# js_model_print = Template("""
# function (n_clicks) {
#         var page =  '$print_page'
#         var n = n_clicks
#         console.log('n')
#         console.log(n)
#         console.log('n_clicks')
#         console.log(n_clicks)
#         console.log(n + '- TESTE-----')
#
#         const content = document.getElementById(page).innerHTML;
#         const printWindow = window.open('', '_blank');
#         printWindow.document.write('<html>');
#
#         printWindow.document.write('<head><title>Print</title></head><body>');
#
#         printWindow.document.write(content);
#         printWindow.document.write('</body></html>');
#         printWindow.document.close();
#         printWindow.print();
#
#         console.log(page)
#
#         return ''
#     }
#     """)

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
    all_columns = cfg_relatorio_simples['radio_itens'][table_radio]['all_columns']
    # columns = cfg_relatorio_simples['radio_itens'][table_radio]['columns']

    opt = []

    for x in filted_columns:
        if all_columns[x]['ckbox'] == True:
            b = {
                "label": x.replace('_', ' ').title(),
                "value": x
            }
            opt.append(b)

    if table_radio == 1:
        """
        NAO FUNCIONA
        """

        check_box = dbc.Checklist(
            options=opt,
            value=default_columns,
            id=f"check-columns-{page_name}",
            inline=True,

        )
    elif table_radio == 2:
        df_turma = dados.query_table(table_name='turma')

        inicio = df_turma['inicio'].min()
        fim = df_turma['fim'].max()

        now = date.today()

        dt_picker =dbc.Card(
            class_name='shadow-lg border mx-1 my-1 px-1 py-1 text-center',
            # class_name='shadow-lg border mx-0 my-1 px-0 py-1 text-middle text-center',
            children=[
                dbc.CardHeader(
                    children=html.P(
                        f'INICIO - FIM',
                        className='p-2 m-2',
                        style={
                            # 'font-weight': 'bold',
                            'font-size': '14px'
                        },
                    ),
                    class_name='py-0 my-0 justify-content-top text-center'
                ),
                dbc.CardBody(
                    class_name='px-0 mx-0 py-0 my-0',
                    children=[
                        dcc.DatePickerRange(
                            id=f'dt-picker-turma-{page_name}',
                            className='',
                            # id_object=f'datepicker_data_referencia_{page_name}',
                            # title='Data',
                            min_date_allowed=inicio,
                            # min_date_allowed=date(2023, 1, 1),
                            # max_date_allowed=fim,
                            # max_date_allowed=date(2050, 1, 1),
                            initial_visible_month=date.today(),
                            display_format='YYYY-MM-DD',
                            start_date=date(now.year, 1, 1),
                            end_date=date(now.year, 12, 31),
                        )
                    ]
                )
            ]
        )


        # check_box = dbc.Checklist(
        #     id=f"check-columns-{page_name}",
        #     options=opt,
        #     value=default_columns,
        #     inline=True,
        #
        # )
        check_box_columns = CheckList(
            id_object=f"check-columns-{page_name}",
            title='FILTRAR COLUNAS',
            options=opt,
            labelCheckedClassName="text-primary",
            inputCheckedClassName="border border-primary bg-primary",
            # value=['id_submercado', 'tipo_energia'],
            value=default_columns,
            inline=True,
            switch=True,
        )
        check_box_columns.load()

        dia_semana = CheckList(
            id_object=f'inp-dia-semana-{page_name}',
            title='DIA DA SEMANA',
            options=[
                {'label': 'Segunda-feira'.upper(),'value': f'Segunda-feira'.upper()},
                {'label': 'Terça-feira'.upper(),'value': f'Terça-feira'.upper()},
                {'label': 'Quarta-feira'.upper(),'value': f'Quarta-feira'.upper()},
                {'label': 'Quinta-feira'.upper(),'value': f'Quinta-feira'.upper()},
                {'label': 'Sexta-feira'.upper(),'value': f'Sexta-feira'.upper()},
                {'label': 'Sábado'.upper(),'value': f'Sábado'.upper()},
                {'label': 'Domingo'.upper(),'value': f'Domingo'.upper()},
            ],
            labelCheckedClassName="text-primary",
            inputCheckedClassName="border border-primary bg-primary",
            # value=['id_submercado', 'tipo_energia'],
            value=[
                'Segunda-feira'.upper(),
                'Terça-feira'.upper(),
                'Quarta-feira'.upper(),
                'Quinta-feira'.upper(),
                'Sexta-feira'.upper(),
            ],
            inline=True,
            switch=True,
        )
        dia_semana.load()

        # dia_semana = dbc.Row(
        #     children=[
        #         dbc.Row('DIA DA SEMANA'),
        #         dbc.Row(
        #             children=[
        #                 dbc.Checklist(
        #                     id=f'inp-dia-semana-{page_name}',
        #                     options=[
        #                         {'label': 'Segunda-feira'.upper(),'value': f'Segunda-feira'.upper()},
        #                         {'label': 'Terça-feira'.upper(),'value': f'Terça-feira'.upper()},
        #                         {'label': 'Quarta-feira'.upper(),'value': f'Quarta-feira'.upper()},
        #                         {'label': 'Quinta-feira'.upper(),'value': f'Quinta-feira'.upper()},
        #                         {'label': 'Sexta-feira'.upper(),'value': f'Sexta-feira'.upper()},
        #                         {'label': 'Sábado'.upper(),'value': f'Sábado'.upper()},
        #                         {'label': 'Domingo'.upper(),'value': f'Domingo'.upper()},
        #                     ],
        #                     inline=True,
        #                     value=[
        #                         'Segunda-feira'.upper(),
        #                         'Terça-feira'.upper(),
        #                         'Quarta-feira'.upper(),
        #                         'Quinta-feira'.upper(),
        #                         'Sexta-feira'.upper(),
        #                     ],
        #                 )
        #             ],
        #         ),
        #     ],
        # className='m-0 pt-2'
        # )

        row_status = DropDownMenu(
            id_object=f'inp-status-turma-{page_name}',
            title='STATUS',
            options=[
                {'label': 'Ativa'.upper(), 'value': f'Ativa'.upper()},
                {'label': 'Inativa'.upper(), 'value': f'Inativa'.upper()},
                {'label': 'Em espera'.upper(), 'value': f'Em espera'.upper()},
                {'label': 'Finalizadas'.upper(), 'value': f'Finalizadas'.upper()},
            ],
            value='ATIVA',
        )
        row_status.load()
        # row_status = dbc.Row(
        #     children=[
        #         dbc.Row('STATUS', className='m-0 p-0'),
        #         dbc.Row(
        #             children=[
        #                 dbc.Select(
        #                     id=f'inp-status-turma-{page_name}',
        #                     options=[
        #                         {'label': 'Ativa'.upper(), 'value': f'Ativa'.upper()},
        #                         {'label': 'Inativa'.upper(), 'value': f'Inativa'.upper()},
        #                         {'label': 'Em espera'.upper(), 'value': f'Em espera'.upper()},
        #                         {'label': 'Finalizadas'.upper(), 'value': f'Finalizadas'.upper()},
        #                     ],
        #                     value='ATIVA',
        #                 )
        #             ],
        #             className='m-0 p-0'
        #         ),
        #     ],
        # className='m-0 pt-2'
        # )

    # row_check_box =  dbc.Row(
    #         children=[
    #             dbc.Row('COLUNAS'),
    #             dbc.Row(check_box),
    #         ],
    #     className='m-0 pt-2'
    #
    # )

    result = dbc.Row(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        className='col-lg-6 col-md-12 col-sm-12',
                        children=[
                            dt_picker,
                        ],
                    ),
                    dbc.Col(
                        className='col-lg-6 col-md-12 col-sm-12',
                        children=[
                            row_status.layout,
                        ],
                    ),
                ],
                class_name='m-0 p-0',
            ),
            dia_semana.layout,
            check_box_columns.layout,
        ],
        className='m-0 pt-2'
    )

    return result

@callback(
    Output(component_id=f'out-edit-funcionario-{page_name}', component_property='children'),
    Output(component_id=f'out-edit-funcionario-print-{page_name}', component_property='children'),

    # Input(component_id=f'main-container-{page_name}', component_property='children'),
    State(component_id=f'dt-picker-turma-{page_name}', component_property='start_date'),
    State(component_id=f'dt-picker-turma-{page_name}', component_property='end_date'),
    State(component_id=f'inp-status-turma-{page_name}', component_property='value'),
    State(component_id=f'inp-dia-semana-{page_name}', component_property='value'),
    State(component_id=f"tabela-options-{page_name}", component_property='value'),
    State(component_id=f"check-columns-{page_name}", component_property='value'),
    Input(component_id=f'btn-buscar-generico-{page_name}', component_property='n_clicks'),
)
def capturar_alunos(
        start_date,
        endt_date,
        status,
        dia_semana,
        table_radio, check_box_columns, btn_buscar):


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

        df_result2 = df_result.copy()

    elif table_radio == 2:
        fixed_columns = cfg_relatorio_simples['radio_itens'][table_radio]['fixed_columns']
        all_columns = cfg_relatorio_simples['radio_itens'][table_radio]['all_columns']
        list_columns = [x for x in fixed_columns] +  check_box_columns

        # query
        # horario = ['']
        # periodo = []
        weekday = dia_semana
        status_turma = status
        dt_inicio = start_date
        dt_fim = endt_date

        # captura horarios
        df_horario  = dados.query_table(table_name='horario',)
        df_horario.rename(columns={'id': 'id_horario'}, inplace=True)

        # captura funcionarios
        df_prof = dados.query_table(
            table_name='funcionario',
            filter_list=[
                {'op': 'in', 'name': 'tipo', 'value': ['Gerente', 'Professor', 'Coordenador']},
                # {'op': 'eq', 'name': 'tipo','value': 'Professor'},
                # {'op': 'eq', 'name': 'tipo','value': 'Gerente'},
            ]
        )


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
                {'op': 'ge', 'name': 'inicio', 'value': dt_inicio},
                {'op': 'le', 'name': 'fim', 'value': dt_fim},
            ]
        )
        df_turma.rename(columns={'status': 'status_turma'}, inplace=True)
        # df_turma.drop(columns=['id_aluno'], inplace=True)

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
        # df_merge_turma2 = df_merge_turma2

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

        # remove id_turma to append horarios
        list_week_days1.remove('id_turma')
        list_columns = list_columns + list_week_days1

        """
        merge professor e coord
        """

        df_merge_4['id_professor'] = df_merge_4['id_professor'].astype(int)
        df_merge_4['id_coordenador'] = df_merge_4['id_coordenador'].astype(int)

        # df_result = df_merge_4[list_columns]
        # df_result = df_merge_4[list_columns]
        # 'nome_professor', 'nome_coordenador', 'escola', 'descricao', 'nivel', 'map', 'idioma',
        # 'inicio_aluno', 'n_irmaos', 'sexo',

        df_user = dados.query_table(
            table_name='user',
            field_list=[
                {'name': 'email'},
                {'name': 'status'},
            ]
        )
        df_user['email_func'] = df_user['email']

        df_prof['id_professor'] = df_prof['id']
        df_prof['id_coordenador'] = df_prof['id']

        df_turma3 = pd.merge(
            left=df_prof[['email_func', 'id_professor', 'nome_completo']],
            right=df_user,
            how='left',
            on=['email_func'],
        )
        df_turma3.rename(
            columns={
                # 'email_func': 'email_prof',
                'nome_completo': 'nome_professor',
            }, inplace=True
        )
        df_turma4 = pd.merge(
            left=df_turma3,
            right=df_prof[['email_func', 'id_coordenador', 'nome_completo']],
            how='left',
            on=['email_func'],
        )
        df_turma4.rename(
            columns={
                # 'email_func': 'email_coord',
                'nome_completo': 'nome_coordenador',
            }, inplace=True
        )

        """
        merge result
        """

        # df_merge_4['id_professor']

        df_result0 = pd.merge(
            left=df_merge_4,
            right=df_turma4[['id_professor', 'nome_professor', 'email_func']],
            how='left',
            on=['id_professor']
        )
        df_result0.rename(columns={'email_func':'email_professor'}, inplace=True)

        df_result1 = pd.merge(
            left=df_result0,
            right=df_turma4[['id_coordenador', 'nome_coordenador', 'email_func']],
            how='left',
            on=['id_coordenador']
        )
        df_result1.rename(columns={'email_func': 'email_coordenador'}, inplace=True)

        # concatenando enderecos
        for x in list_columns:
            if '/' in x:
                aux = x.split('/')
                df_result1[x] = df_result1[aux[0]] + ' ' +  df_result1[aux[0]]

        # filter data columns
        df_result2 = df_result1[list_columns]
        # df_result = df_result2.set_axis(list_columns, axis=1,)

    columns = [
        {
            "id": all_columns[i]['id'],
            "name": all_columns[i]['nome'].replace('_', ' ').upper(),
            "type": all_columns[i]['type'],
            # "editable": True if filted_columns[i]['type'] == 1 else False,
            # "presentation": 'dropdown' if i == 'cadastrado' else '',
        } for i in list_columns
    ]

    # columns = [
    #     {
    #         "id": filted_columns[i]['id'],
    #         "name": filted_columns[i]['nome'].replace('_', ' ').upper(),
    #         "type": filted_columns[i]['type'],
    #         # "editable": True if filted_columns[i]['type'] == 1 else False,
    #         # "presentation": 'dropdown' if i == 'cadastrado' else '',
    #     } for i in list_columns
    # ]

    # DASH DATA TABLE
    dt = dash_table.DataTable(
        id=f'data-table-edit-user-{page_name}',
        # filtrando data frame
        data=df_result2[list_columns].to_dict('records'),
        # data=df_result[list_columns].to_dict('records'),
        columns=columns,
        # row_deletable=True,
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
        style_header={
            'textAlign': 'left',
            'fontWeight': 'bold'
        },
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': col},
                'textAlign': 'left'
            } for col in [list_columns]
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

    """
    loop para criar tabelas separadas por pag
    """

    # removendo colunas que possuem linhas reptidas
    # para plotar uma tabela mais limpa


    # # removendo
    # if 'id_turma' in list_columns:
    #     list_columns.remove('id_turma')
    #
    # if 'status_turma' in list_columns:
    #     list_columns.remove('id_turma')

    list_tables_print = []
    for turma_id in df_result2['id_turma'].unique():

        list_columns2 = list_columns.copy()

        # filtrar turma por id
        df_result_x = df_result2[df_result2['id_turma'] == turma_id]

        # stt = df_result_x['status_turma'].unique()[0]
        # removendo
        if 'id_turma' in list_columns2:
            list_columns2.remove('id_turma')
            df_result_x.drop(columns=['id_turma'], inplace=True)

        if 'status_turma' in list_columns2:
            list_columns2.remove('id_turma')
            df_result_x.drop(columns=['status_turma'], inplace=True)

        nome_professor = ''
        if 'nome_professor' in list_columns2:
            list_columns2.remove('nome_professor')
            nome_professor = df_result_x['nome_professor'].unique()[0]
            df_result_x.drop(columns=['nome_professor'], inplace=True)

        nome_coordenador = ''
        if 'nome_coordenador' in list_columns2:
            list_columns2.remove('nome_coordenador')
            nome_coordenador = df_result_x['nome_coordenador'].unique()[0]
            df_result_x.drop(columns=['nome_coordenador'], inplace=True)

        escola = ''
        if 'escola' in list_columns2:
            list_columns2.remove('escola')
            escola = df_result_x['escola'].unique()[0]
            df_result_x.drop(columns=['escola'], inplace=True)

        escola_info = dbc.Row(
            class_name='pt-2',
            children=[
                html.H6(
                    children=[
                        f'Prof.: {nome_professor}'.upper()
                    ],
                ),
                html.H6(
                    children=[
                        f'Coord.: {nome_coordenador}'.upper()
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
        rows_horarios = list()
        for week in list_week_days:

            # captura hora da turma
            hr_turma = str(df_result_x[f'horario-{week}'].unique()[0])

            # validando se coluna está vazia
            if hr_turma != 'nan':
                """
                adiciona horario na linha quando col não for vazia
                """
                # rows_horarios.append(
                #     f"{week} {df_result_x[f'horario-{week}'].unique()[0]}".upper()
                # )

                rows_horarios.append(
                    dbc.Row(
                        children=[
                            dbc.Col(
                                class_name='col-4',
                              children=[
                                  f"{week} ".upper()
                              ]
                            ),
                            dbc.Col(
                                class_name='col-4',
                              children=[
                                  f"{df_result_x[f'horario-{week}'].unique()[0]}".upper()
                              ]
                            ),
                            dbc.Col(
                                class_name='col-10',
                            ),
                            # f"{week} {df_result_x[f'horario-{week}'].unique()[0]}".upper()
                            # f"{week} {df_result_x[f'horario-{week}'].unique()[0]}".upper()
                        ],
                        # class_name='m-0 p-0'
                    )
                )
                rows_horarios.append(html.Br())
            # else:

            # apagando coluna
            df_result_x.drop(columns=[f'horario-{week}'], inplace=True)

            # removendo col da lista
            list_columns2.remove(f'horario-{week}')


        # criar colunas
        columns = [
            {
                "id": all_columns[i]['id'],
                "name": all_columns[i]['nome'].replace('_', ' ').upper(),
                "type": all_columns[i]['type'],
                # "editable": True if filted_columns[i]['type'] == 1 else False,
                # "presentation": 'dropdown' if i == 'cadastrado' else '',
            } for i in list_columns2
        ]

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
                                    html.H6(
                                        className='pt-2',
                                        children=rows_horarios,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                class_name='col-3',
                                children=escola_info
                            )
                        ],
                    ),

                    # html.Hr(),

                    dash_table.DataTable(
                        id=f'data-table-edit-user-{page_name}-{turma_id}',
                        data=df_result_x[list_columns2].to_dict('records'),
                        columns=columns,
                        editable=False,
                        page_action="native",
                        style_header={
                            'textAlign': 'left',
                            'fontWeight': 'bold'
                        },
                        style_cell_conditional=[
                            {
                                'if': {'column_id': col},
                                'textAlign': 'left'
                            } for col in [list_columns2]
                        ],
                        style_as_list_view=True,
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

    datatable1 = dbc.Row(dt, class_name='col-lg-12 col-md-12 col-sm-12 overflow-auto p-0 m-0')

    # return output_print
    return datatable1, output_print
