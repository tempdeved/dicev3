import glob
import os.path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from utils.create_excel import Turma_xlsx

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
page_name = 'Diploma'
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
                                                        label="ALUNOS",
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
                                                                                id=f'btn-download-turma-{page_name}',
                                                                                children=['DOWNLOAD'],
                                                                                class_name='me-0',
                                                                                color='primary',
                                                                                n_clicks=0,
                                                                            ),
                                                                            dcc.Download(
                                                                                id=f"out-download-turma-{page_name}")
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
    Output(component_id=f"out-download-turma-{page_name}", component_property="data"),
    State(component_id=f'data-table-hist-aluno-{page_name}', component_property="data"),
    # State(component_id=f'data-table-edit-user-{page_name}', component_property="data"),
    Input(component_id=f'btn-download-turma-{page_name}', component_property="n_clicks"),
    prevent_initial_call=True,
)
def func(df_raw, n_clicks):
    if df_raw:
        # path_folder = 'download'
        # filename = page_name + '.png'

        format_file = 'png'
        file_path = os.path.join('static', 'images', 'certificate', f'cert.{format_file}')

        #
        # # delete xlsx files
        # for f in glob.iglob(path_folder + '/*.xlsx', recursive=True):
        #     os.remove(f)
        #
        # df = pd.DataFrame(data=df_raw)
        #
        # # create file
        # Turma_xlsx(file_path=file_path, df=df)

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
    # Input(component_id=f"mes-ref-{page_name}",  component_property='value'),
    # prevent_initial_callbacks=True,
    )
def editar_turma(data_drom_data_table, active_cell):

    if data_drom_data_table and active_cell:

        df_turma = pd.DataFrame(data_drom_data_table)

        turma_id = df_turma['id'].iloc[active_cell[0]]
        turma_id_dice = df_turma['id_turma'].iloc[active_cell[0]]
        id_turma_dice = int(df_turma['id_turma'].iloc[active_cell[0]])

        df_turma2  = dados.query_table(
            table_name='turma_aluno',
            # field_list=[
            #     {'name': 'email'},
            # ],
            filter_list=[
                {'op': 'eq', 'name': 'id_turma', 'value': f'{turma_id_dice}'},
            ]
        )
        df_turma2.drop(
            columns=['id'],
            inplace=True
        )

        df_all_aluno  = dados.query_table(
            table_name='aluno',
            # field_list=[
            #     {'name': 'descricao'},
            # ],
            filter_list=[
                {'op': 'in', 'name': 'id', 'value': df_turma2['id_aluno'].to_list()},
            ]
        )

        df_merge = pd.merge(
            left=df_turma2,
            right=df_all_aluno.rename(columns={'id':'id_aluno'}),
            how='left',
            on=['id_aluno'],
        )

        list_columns = [
            'id_turma',
            'id_aluno',
            'nome',
        ]

        df_merge = df_merge[list_columns]

        dt_turma = dash_table.DataTable(
            id=f'data-table-hist-aluno-{page_name}',
            data=df_merge.to_dict('records'),
            columns=[
                {
                    "id": i,
                    "name": i.replace('_', ' ').upper(),
                    # "type": i,
                    # "editable": True if i == 1 else False,
                    # "presentation": 'dropdown' if i == 'cadastrado' else '',
                 } for i in df_merge.columns
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
            # page_size=30,
            # filter_action='native',
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
    # State(component_id=f"mes-ref-{page_name}", component_property='value'),
    # State(component_id=f'data-table-edit-user-{page_name}', component_property='data'),
    State(component_id=f'data-table-hist-aluno-{page_name}', component_property='data'),
    Input(component_id=f'data-table-hist-aluno-{page_name}', component_property='selected_rows'),
)
def edit_remart(
        dt_alu_tur,
        active_cell
):

    if dt_alu_tur and active_cell:
        df_alu_turma = pd.DataFrame(dt_alu_tur)

        # turma_id =  df_turma['id_turma'].iloc[active_cell[0]]
        # turma_id_dice = df_turma['id_turma'].iloc[active_cell[0]]
        id_turma = int(df_alu_turma['id_turma'].iloc[active_cell[0]])
        nome_aluno = str(df_alu_turma['nome'].iloc[active_cell[0]])

        static_path_file = '/static/images/certificate/'
        name_file = 'cert_dummy'
        format_file = 'png'

        path_static_orig = f'{static_path_file}{name_file}.{format_file}'
        path_static_new = f'{static_path_file}cert.{format_file}'

        path_file = os.path.join('static', 'images', 'certificate', f'{name_file}.{format_file}')

        image = Image.open(path_file)

        myFont = ImageFont.truetype(font='arial.ttf', size=65)

        # tamanho img
        size = image.size
        W, H = size

        # instanciando para editar
        draw = ImageDraw.Draw(image)

        # capturando ?????
        _, _, w, h = draw.textbbox((0, 0), nome_aluno, font=myFont)

        # escrevendo na img
        draw.text(
            ((W - w) / 2, (H - h) / 2),
            nome_aluno,
            font=myFont,
            fill='black'
        )

        # image.show()

        os.remove(
            os.path.join('static', 'images', 'certificate', f'cert.{format_file}')
        )
        image.save(
            os.path.join('static', 'images', 'certificate', f'cert.{format_file}')
        )

        certi_png = html.Img(
                        src=path_static_new,
                        alt='certificado',
                        # className='perfil_avatar mx-auto',
                        # style={'height': '120px', 'width': '270px'},
        )

        editable_remark = dbc.Row(
            children=[
                ''
                # certi_png
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