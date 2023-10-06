import datetime
import locale
from dash import html, dcc
import dash_bootstrap_components as dbc
from elements.dropdown import DropDownMenu
from banco.rodadas.dados import Dados
from utils.utils import Utils
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class StudiesDropdown(object):

    def __init__(self):
        ...

    def get_study_options(self):
        dados = Dados()
        df_options = dados.get_unique_studies(study_type='medio-prazo-historico')
        df_options = Utils().transform_nom_estudo(df=df_options, tag='longo-prazo-comparativo')
        df_options.sort_values(by=['cod_estudo'], ascending=False, inplace=True)
        options = [{'label': row['nom_estudo'], 'value': row['id']} for i, row in df_options.iterrows()]

        return options

    def curto_prazo(self,
                    id_name=None,
                    title='CONTROLES',
                    study_type='all',
                    dropdown_input=None,
                    ssis_selector='sudeste',
                    multiple_inputs=False
                    ):
        options = [
            {'label': 'Sudeste', 'value': 'sudeste'},
            {'label': 'Sul', 'value': 'sul'},
            {'label': 'Nordeste', 'value': 'nordeste'},
            {'label': 'Norte', 'value': 'norte'}
        ]

        dados = Dados()

        df = dados.get_unique_studies(study_type=study_type)

        # filtrar tipo de rodada
        df_estudo = df[df['nom_dash'] == study_type]

        df_estudo_dropdown = Utils().transform_nom_estudo(df=df_estudo, tag=study_type)

        df_estudo_dropdown = df_estudo_dropdown.sort_values(by="dat_pub", ascending=False)

        max_index = df_estudo_dropdown[df_estudo_dropdown["dat_pub"] == df_estudo_dropdown["dat_pub"].max()].set_index('id').index[0]

        # set study_id
        if dropdown_input == None:
            study_id = int(max_index)
            agrupamento = ssis_selector
        else:
            study_id = int(dropdown_input)
            agrupamento = ssis_selector

        # Getting and formatting data for dropdown
        dropdown_study = DropDownMenu().layout(
            id_name=id_name,
            options=[
                {'label': row["nom_estudo"], 'value': row["id"]}
                for index, row in df_estudo_dropdown.iterrows()
            ],
            multiple_inputs=multiple_inputs,
            default_values=study_id,
        )

        if agrupamento == 'False':
            seletor = html.Div()
            classname_selector = 'col-sm-12 col-lg-12 py-2'
        else:
            classname_selector = 'col-sm-12 col-lg-10 py-2 '
            dropdown_agrupamento = DropDownMenu().layout(
                id_name='agrupamento',
                options=options,
                multiple_inputs=False,
                default_values=agrupamento,
            )
            seletor = dbc.Col(
                class_name='col-lg-2 col-sm-12',
                children=
                [html.Div(
                    children=[dropdown_agrupamento],
                )],
            ),

        # Dropdown menu filling
        current_year = datetime.datetime.now().year
        years = range(2000, current_year)
        # years_marks = {str(k): str(k) for k in years}
        # default_years = [2000, 2006, 2015, current_year - 1]

        # Controles de seleção de estudo e filtro dos cenários históricos
        layout = dbc.Row(
            id='',
            class_name='px-0 mx-0',
            children=[
                dbc.Row(
                    class_name='px-0 py-2 mx-0 justify-content-center',
                    id='',
                    children=[

                        dbc.Accordion(
                            id='',
                            class_name='px-0 py-2 mx-0',
                            children=[

                                dbc.AccordionItem(
                                    id='',
                                    class_name='',
                                    title=title,
                                    children=[

                                        # dbc.Card(
                                        #     id='',
                                        #     class_name='px-0 mx-0 shadow',
                                        #     children=[

                                                # Controle de seleção de estudo
                                                dbc.Row(
                                                    class_name='px-0 mx-0',
                                                    id='dropdown-case-selection',
                                                    children=[
                                                        dbc.Col(
                                                            class_name=classname_selector,
                                                            children=[
                                                                html.Div(
                                                                    children=[dropdown_study],
                                                                )
                                                            ],
                                                        ),
                                                        seletor,
                                                        # dbc.Col(
                                                        #     class_name='col-md-2 col-sm-12',
                                                        #     children=
                                                        #     [html.Div(
                                                        #         children=[dropdown_agrupamento],
                                                        #     )],
                                                        # )
                                                    ],
                                                ),
                                                # check list
                                                html.Div(id=f'check-list-ena',
                                                         children=[
                                                             dbc.RadioItems(
                                                                 id=f'dcc-checklist-{id_name}',
                                                                 # options=['config'],
                                                                 options=[
                                                                     {'label': 'Semanal', 'value': 'semanal'},
                                                                    {'label': 'Mensal', 'value': 'mensal'},
                                                                 ],
                                                                 value='semanal',
                                                                 inline=True,
                                                             )
                                                         ]
                                                         ),
                                            # ]
                                        # ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ]
        )

        # return dropdown_study
        return layout

    def medio_prazo_historico(self, id_name=None,
                              title='CONTROLES',
                              study_type='all',
                              dropdown_input=None,
                              ssis_selector='sudeste',
                              multiple_inputs=False,
                              slider=False
                              ):
        options = [
            {'label': 'Sudeste', 'value': 'sudeste'},
            {'label': 'Sul', 'value': 'sul'},
            {'label': 'Nordeste', 'value': 'nordeste'},
            {'label': 'Norte', 'value': 'norte'}
        ]

        dados = Dados()

        df = dados.get_unique_studies(study_type=study_type)

        # filtrar tipo de rodada
        df_estudo = df[df['nom_dash'] == study_type]

        df_estudo_dropdown = Utils().transform_nom_estudo(df=df_estudo, tag=study_type)


        if study_type == 'longo-prazo-agregado':
            max_index = df_estudo_dropdown[df_estudo_dropdown["dat_pub"] == df_estudo_dropdown["dat_pub"].max()].set_index('dat_pub').index[0]
            flag_dropdown = 'dat_pub'
            if dropdown_input == None:
                study_id = max_index
                agrupamento = ssis_selector
            else:
                study_id = dropdown_input
                agrupamento = ssis_selector
        else:
            max_index = df_estudo_dropdown[df_estudo_dropdown["dat_pub"] == df_estudo_dropdown["dat_pub"].max()].set_index('id').index[0]
            flag_dropdown = 'id'
            # set study_id
            if dropdown_input == None:
                study_id = int(max_index)
                agrupamento = ssis_selector
            else:
                study_id = int(dropdown_input)
                agrupamento = ssis_selector
        # df = df.sort_values(by="dat_pub", ascending=False)

        df_estudo_dropdown = df_estudo_dropdown.sort_values(by="dat_pub", ascending=False)

        # # set study_id
        # if dropdown_input == None:
        #     study_id = int(max_index)
        #     agrupamento = 'Sudeste'
        # else:
        #     study_id = int(dropdown_input)
        #     agrupamento = 'Sudeste'

        # Getting and formatting data for dropdown
        dropdown_study = DropDownMenu().layout(
            id_name=id_name,
            options=[
                {'label': row["nom_estudo"], 'value': row[flag_dropdown]}
                for index, row in df_estudo_dropdown.iterrows()
            ],
            multiple_inputs=multiple_inputs,
            default_values=study_id,
        )

        if agrupamento == 'False':
            seletor = html.Div()
            classname_selector = 'col-sm-12 col-lg-12 py-2'
        else:
            classname_selector = 'col-sm-12 col-lg-10 py-2 '
            dropdown_agrupamento = DropDownMenu().layout(
                id_name='agrupamento',
                options=options,
                multiple_inputs=False,
                default_values=agrupamento,
            )
            seletor = dbc.Col(
                class_name='col-lg-2 col-sm-12',
                children=
                [html.Div(
                    children=[dropdown_agrupamento],
                )],
            ),


        # Dropdown menu filling
        current_year = datetime.datetime.now().year
        years = range(2000, current_year)
        years_marks = {str(k): str(k) for k in years}
        default_years = [current_year - 10, current_year - 3, current_year - 2, current_year - 1]
        # default_years = [2000, 2006, 2015, current_year - 1]

        if slider:
            range_slider = dcc.RangeSlider(
                id=f'rng-slider-anos-{id_name}',
                className='px-0',
                min=2000,
                max=current_year - 1,
                step=1,
                marks=years_marks,
                allowCross=False,
                value=default_years,
                pushable=1,
                tooltip={
                    "placement": "bottom",
                    "always_visible": False
                }
            )
        else:
            range_slider = ''

        # Controles de seleção de estudo e filtro dos cenários históricos
        layout = dbc.Row(
            id='',
            class_name='px-0 mx-0',
            children=[
                dbc.Row(
                    class_name='px-0 py-2 mx-0 justify-content-center',
                    id='',
                    children=[

                        dbc.Accordion(
                            id='',
                            class_name='px-0 py-2 mx-0',
                            children=[

                                dbc.AccordionItem(
                                    id='',
                                    class_name='',
                                    title=title,
                                    children=[
                                                # Controle de seleção de estudo
                                                dbc.Row(
                                                    class_name='px-0 mx-0',
                                                    id='dropdown-case-selection',
                                                    children=[
                                                        dbc.Col(
                                                            class_name=classname_selector,
                                                            # class_name='col-md-10 col-sm-12',
                                                            children=[
                                                                html.Div(
                                                                    children=[dropdown_study],
                                                                )
                                                            ],
                                                        ),
                                                        seletor,
                                                        # dbc.Col(
                                                        #     class_name='col-md-2 col-sm-12',
                                                        #     children=
                                                        #     [html.Div(
                                                        #         children=[dropdown_agrupamento],
                                                        #     )],
                                                        # ),
                                                    ],
                                                ),
                                                dbc.Row(
                                                    id=f'fitering-controls-{id_name}',
                                                    class_name='px-0 mx-0 justify-content-center '
                                                               'text text-center',
                                                    children=[
                                                        dbc.Col(
                                                            class_name='col-sm-12 col-lg-10 py-2 ',
                                                            children=[range_slider]
                                                        )
                                                    ]
                                                ),
                                                # check list
                                                # html.Div(id=f'check-list-ena',
                                                #          children=[
                                                #              dbc.Checklist(
                                                #                  id=f'dcc-checklist-{id_name}',
                                                #                  # options=['config'],
                                                #                  options=options,
                                                #                  value=['sudeste', 'sul', 'nordeste', 'norte', ],
                                                #                  inline=True,
                                                #              )
                                                #          ]
                                                #          ),
                                            # ]
                                        # ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ]
        )

        # return dropdown_study
        return layout

    def load(self, id_name, title='CONTROLES'):

        study_options = self.get_study_options()

        # Getting and formatting data for dropdown
        options = DropDownMenu().layout(
            id_name=id_name,
            options=self.get_study_options(),
            multiple_inputs=True,
            default_values=[study_options[0]['value']]
        )

        # Dropdown menu filling
        current_year = datetime.datetime.now().year
        years = range(2000, current_year)
        years_marks = {str(k): str(k) for k in years}
        default_years = [2000, 2006, 2015, current_year - 1]

        # Controles de seleção de estudo e filtro dos cenários históricos
        layout = dbc.Row(
            id='',
            class_name='px-0 mx-0',
            children=[
                dbc.Row(
                    class_name='px-0 py-2 mx-0 justify-content-center',
                    id='',
                    children=[

                        dbc.Accordion(
                            id='',
                            class_name='px-0 py-2 mx-0',
                            children=[

                                dbc.AccordionItem(
                                    id='',
                                    class_name='',
                                    title=title,
                                    children=[

                                        dbc.Card(
                                            id='',
                                            class_name='px-0 mx-0 shadow',
                                            children=[

                                                # Controle de seleção de estudo
                                                dbc.Row(
                                                    class_name='px-0 mx-0',
                                                    id='dropdown-case-selection',
                                                    children=options,
                                                ),

                                                # Controles de filtro do estudo
                                                dbc.Row(
                                                    id='fitering-controls',
                                                    class_name='px-0 mx-0 justify-content-center '
                                                               'text text-center',
                                                    children=[
                                                        dbc.Col(
                                                            class_name='col-sm-12 col-lg-10 py-2 ',
                                                            children=[
                                                                dcc.RangeSlider(
                                                                    id='rng-slider-anos',
                                                                    className='px-0',
                                                                    min=2000,
                                                                    max=current_year - 1,
                                                                    step=1,
                                                                    marks=years_marks,
                                                                    allowCross=False,
                                                                    value=default_years,
                                                                    pushable=1,
                                                                    tooltip={
                                                                        "placement": "bottom",
                                                                         "always_visible": False
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ]
        )

        return layout
