import datetime

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
from utils.get_idade import CalculateAge

from string import Template

# page_name = __name__[6:].replace('.', '_')
page_name='RelatorioAlunoGenerico'
dash.register_page(__name__, path=f'/{page_name}')

config = Config().config
dados = Dados(config['ambiente'])
cfg_relatorio_simples = config['relatorio_simples']

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
                                                            {"label": "Somente alunos", "value": '1'},
                                                            {"label": "Alunos P/ Turmas", "value": '2'},
                                                        ],
                                                        value='1',
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
                                        title="Relatório Aluno Genérico"
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

# printWindow.document.write('<script src="https://cdn.plot.ly/plotly-locale-pt-br-latest.js"></script>');
# printWindow.document.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/zephyr/bootstrap.min.css">');
# printWindow.document.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap-grid.min.css">');
# printWindow.document.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">');
# printWindow.document.write('<script src="https://cdn.plot.ly/plotly-locale-pt-br-latest.js"></script>');
# printWindow.document.write('<script src="https://cdn.plot.ly/plotly-locale-pt-br-latest.js"></script>');
# theme
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/zephyr/bootstrap.min.css">
# grid
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap-grid.min.css">
# icon
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
# theme
# https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/
# https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/zephyr/bootstrap.min.css

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

    if table_radio == 1:

        check_box = dbc.Checklist(
            options=[
                {
                    "label": x.replace('_', ' ').title(),
                    "value": x
                }
                for x in filted_columns
            ],
            value=default_columns,
            id=f"check-columns-{page_name}",
            inline=True,

        )
    elif table_radio == 2:
        check_box = dbc.Checklist(
            options=[
                {
                    "label": x.replace('_', ' ').title(),
                    "value": x
                }
                for x in filted_columns
            ],
            value=default_columns,
            id=f"check-columns-{page_name}",
            inline=True,

        )
        date_range = dcc.DatePickerRange(

        )



    result = dbc.Row(
        children=[
            date_range,
            check_box
        ]
    )

    return result

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
        # today.year - birthDate.year -
        #          ((today.month, today.day) <
        #          (birthDate.month, birthDate.day))
        now = datetime.datetime.now()
        # resebendo resultado
        df_result = df_bruto.copy()

        # df_result['dat_nasc'] = pd.to_datetime(df_result['dat_nasc'])
        # df_result['idade'] = df_result['dat_nasc'].apply(CalculateAge)

    elif table_radio == 2:

        # query
        df_bruto = dados.query_table(table_name=table_name)
        df_aluno  = dados.query_table(table_name='aluno',)
        df_turma  = dados.query_table(table_name='turma',)
        df_horario  = dados.query_table(table_name='horario',)

        # rename id_horario
        df_horario.rename(columns={'id':'id_horario'}, inplace=True)

        # rename aluno
        df_aluno.rename(
            columns={
                'id': 'id_aluno',
                'status': 'status_aluno',
                'inicio': 'inicio_aluno',
            },
            inplace=True
        )

        # rename turma
        df_turma.rename(
            columns={
                'status': 'status_turma',
                'inicio': 'inicio_turma',
                'fim': 'fim_turma',
            },
            inplace=True
        )
        df_turma.drop(columns=['id', 'id_aluno'], inplace=True)

        df_merge = pd.merge(
            left=df_bruto,
            right=df_aluno,
            on=['id_aluno'],
            how='left',
        )
        # merge
        df_merge2 = pd.merge(
            left=df_merge,
            right=df_turma,
            on=['id_turma'],
            how='left',
        )

        df_merge2.sort_values(
            by=['id_turma', 'status_turma', 'nome'],
            ascending=[False, True, True],
            inplace=True
        )

        # recebendo colunas filtradas
        list_columns = check_box_columns

        df_result = df_merge2.copy()

        tt = df_merge2[list_columns]
        aa = [
                {
                    "id": filted_columns[i],
                    "name": filted_columns[i]['nome'].replace('_', ' ').upper(),
                    "type": filted_columns[i]['type'],
                } for i in list_columns
            ]
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
        filter_action='native',
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
