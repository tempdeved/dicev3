import pandas as pd
import dash_bootstrap_components as dbc
from datetime import timedelta
from dash import html
from bs4 import BeautifulSoup
from config.config import Config
from functools import reduce


class Utils(object):

    def __init__(self):
        ...

    def pivot_rodada_medio_prazo(self,
                                 df: pd.DataFrame,
                                 values: list,
                                 columns_group: list,
                                 index: list,
                                 ssis_selector: str,
                                 table_type: dict,
                                 ):

        # df_filted = df[df['nom_ssis'] == ssis_selector.lower()]
        df_filted = df

        if 'arm' in table_type:
            # df_filted = df[df[table_type['arm']] == "original"]
            df_filted = df_filted[df_filted[table_type['arm']] == "original"]

        df_pivot = df_filted.pivot_table(
            values=values,
            columns=columns_group,
            index=index,
            aggfunc='first', fill_value=''
        )

        df_pivot.rename(columns={"original": "Base"}, inplace=True)

        cols = list(df_pivot.columns)
        cols.sort(reverse=True)
        df_pivot = df_pivot.reindex(columns=cols)


        # order by ssis
        df_pivot.sort_index(level=0, axis=1, ascending=False, inplace=True)
        # df_pivot["Média"] = df_pivot.mean(axis=1)

        return df_pivot

        # aux var
        # aux_base_ena = dado_estudo_pivot_ena[(f'ENA-{ssis_selector}', 'Base')]
        # aux_media_ena = dado_estudo_pivot_ena[('Média', '')]
        # aux_base_preco = dado_preco_pivot[(f'{config["renaming"]["val_preco"]} {ssis_selector}', 'Base')]
        # aux_media_preco = dado_preco_pivot[('Média', '')]

        # remove columns
        # dado_estudo_pivot_ena.drop(columns=[(f'ENA-{ssis_selector}', 'Base'), ('Média', '')], inplace=True)

    def filter_yers_by_columns(self, df: pd.DataFrame, range_slider: list):
        for column in df.columns:
            if (int(column[1]) >= int(range_slider[0])) & (int(column[1]) <= int(range_slider[1])):
                pass
            elif (int(column[1]) >= int(range_slider[2])) & (int(column[1]) <= int(range_slider[3])):
                pass
            else:
                df.drop(columns=[column], inplace=True)
        return df

    def filter_yers_by_columns_unified(self, df: pd.DataFrame, range_slider: list):
        for column in df.columns:
            try:
                if (int(column[1]) >= int(range_slider[0])) & (int(column[1]) <= int(range_slider[1])):
                    pass
                elif (int(column[1]) >= int(range_slider[2])) & (int(column[1]) <= int(range_slider[3])):
                    pass
                else:
                    print(f'apagar coluna{column}')
                    df.drop(columns=[column], inplace=True)
            except:
                print(f'original  {column}')
                # df.drop(columns=[column], inplace=True)
        return df

    def merge_dfs(self, list_of_dfs):
        # Merge DataFrames in list
        merged_df = reduce(lambda left, right:
                           pd.merge(left, right, how="outer"),
                           list_of_dfs)
        return merged_df

    def transform_nom_estudo(self, df, tag):
        df = df
        if 'longo-prazo-agregado' in tag:
            df["nom_estudo"] = df.apply(
                axis=1,
                func=lambda x: f"Estudo Agregado: {x['dat_pub']:%d-%b-%y}     | " +
                               f"Proj: {x['dat_ini'] + timedelta(days=7):%b/%y}  -  " +
                               f"{x['dat_fim'] + timedelta(days=7): %b/%y}"
                               # f"Desc: LPA_{x['nom_estudo'].split('_')[-1].replace('-', ' ')}"[-4:]

            )
        elif 'longo-prazo-comparativo' in tag:
            df["nom_estudo"] = df.apply(
                axis=1,
                func=lambda x: f"Estudo: {x['dat_pub']:%d-%b-%y}     | " +
                               f"Proj: {x['dat_ini'] + timedelta(days=7):%b/%y}  -  " +
                               f"{x['dat_fim'] + timedelta(days=7): %b/%y}"
                # f"Desc: LPA_{x['nom_estudo'].split('_')[-1].replace('-', ' ')}"[-4:]

            )
        elif 'medio-prazo-historico' in tag:
            df["nom_estudo"] = df.apply(
                axis=1,
                func=lambda x: f"Estudo: {x['dat_pub']:%d-%b-%y}| " +
                               f"Proj: {x['dat_ini'] + timedelta(days=7):%b/%y}  -  " +
                               f"{x['dat_fim'] + timedelta(days=7): %b/%y} " +
                               f"Desc: {x['nom_estudo'].split('_')[-1].replace('-', ' ')}"

            )
        else:
            from string import digits
            remove_digits = str.maketrans('', '', digits)
            df["nom_estudo"] = df.apply(
                axis=1,
                func=lambda x: f"Dia: {x['dat_pub']:%d/%b/%y} - " +
                               f"Proj: {x['dat_ini'] + timedelta(days=7):%b/%y} " +
                               f"- {x['nom_estudo'].split('_')[-1].replace('-', ' ')[-10:].translate(remove_digits)}"
                               # f"{x['dat_fim'] + timedelta(days=7): %b/%y} - "
                               # f"Proj: {x['dat_ini'] + timedelta(days=7):%b/%y} a " +


            )

        return df

    def transform_to_dropdown_options(self, option_list: list) -> list:

        options = [{k: k for k in option_list}]

        return options

    def arred_values_on_dataframe(self, df: pd.DataFrame, cols_to_float: dict, cols_to_int: dict, cols_to_percentage: dict) -> pd.DataFrame:


        for int_column in cols_to_int['col_names']:

            df[int_column] = df[int_column].astype(cols_to_int['format'])

        for float_column in cols_to_float['col_names']:
            df[float_column] = df[float_column].round(decimals=cols_to_float['format'])


        for percentage_col in cols_to_percentage['col_names']:
            df[percentage_col] = df[percentage_col].astype(float)
            df[percentage_col] = df[percentage_col].round(decimals=cols_to_percentage['format'])


        return df

    def convert_to_html_table(self, df: pd.DataFrame, th_css: str, tbody_css: str) -> dict:

        config = Config().config
        td_format = config['variables']['formatting'][df.columns.get_level_values(level=0).unique()[0]]

        html_table = df.to_html()
        soup = BeautifulSoup(html_table, 'html.parser')

        headers = soup.find_all(name='thead')[0]
        t_body = soup.find_all(name='tbody')[0]
        table_values = html.Tbody(children=[], className=tbody_css)
        table_headers = html.Thead(children=[], className=th_css)

        # building headers
        for tr_value in headers.children:

            if tr_value.text != '\n':
                tr = html.Tr(children=[])

                for th_value in tr_value:

                    if th_value.text != '\n':

                        try:
                            if th_value.text in config['variables']['renaming']:
                                th = html.Th(
                                    children=config['variables']['renaming'][th_value.text],
                                    colSpan=th_value.attrs['colspan'],
                                    className=th_css
                                )
                            else:
                                th = html.Th(children=th_value.text, colSpan=th_value.attrs['colspan'], className=th_css)
                        except:
                            if th_value.text in config['variables']['renaming']:
                                th = html.Th(
                                    children=config['variables']['renaming'][th_value.text], className=th_css
                                )
                            else:
                                th = html.Th(children=th_value.text, className=th_css)

                        tr.children.append(th)

                table_headers.children.append(tr)

        # building tbody/body
        for tr_value in t_body.children:

            if tr_value.text != '\n':
                tr = html.Tr(children=[])

                for cell_value in tr_value:

                    if cell_value.text != '\n':
                        if cell_value.name == 'th':
                            try:
                                cell = html.Th(children=cell_value.text, rowSpan=cell_value.attrs['rowspan'])
                            except:
                                cell = html.Th(children=cell_value.text)

                        else:
                            try:
                                cell = html.Td(children='{:{}}'.format(float(cell_value.text), td_format))
                            except:
                                pass

                        tr.children.append(cell)

                table_values.children.append(tr)


        return {'thead': table_headers, 'tbody': table_values}

    def generic_table(self,
                      html_table: BeautifulSoup(),
                      table_type: str,
                      class_name: str,
                      title: str,
                      id: str,
                      ):

        # config
        config = Config().config['rodadas']
        config_carga = Config().config['carga']
        config_gd = Config().config['gd']

        soup = BeautifulSoup(html_table, 'html.parser')

        thead = soup.thead
        tbody = soup.tbody

        tbody_list = []
        tr_thead = []

        # Create Thead
        flag = 0
        for tr in thead.find_all('tr'):
            th_list = []

            for th in tr.find_all('th'):
                try:
                    if th.text == '' and flag == 0:
                        content = title
                        flag = 1
                    else:
                        content = th.text
                except:
                    # content = ''
                    content = title

                try:
                    attrs = th.attrs
                    colspan = int(attrs['colspan'])
                except:
                    attrs = {'colspan': 0}
                    colspan = int(attrs['colspan'])

                th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}'))

            tr_thead.append(html.Tr(th_list))

        thead = [html.Thead(children=tr_thead, className='')]

        # Create Tbody
        for tr in tbody.find_all('tr'):
            th_list = []

            td_list = tr.find_all('td')
            len(td_list)
            for th in tr.find_all('th'):
                try:
                    content = th.text
                except:
                    content = ''

                try:
                    attrs = th.attrs
                    colspan = int(attrs['colspan'])
                except:
                    attrs = {'colspan': 0}
                    colspan = int(attrs['colspan'])

                th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}'))
                for td in td_list:
                    try:
                        content_td = td.text
                    except:
                        content_td = ''
                    try:
                        attrs_td = td.attrs
                        colspan_td = int(attrs_td['colspan'])
                    except:
                        attrs_td = {'colspan': 0}
                        colspan_td = int(attrs_td['colspan'])

                    if table_type == config['renaming']['val_preco']:
                        if content_td != '':
                            th_list.append(html.Td(f'{float(content_td):{config["formatting"]["val_preco"]}}', colSpan=f'{colspan_td}', className=f''))
                        else:
                            th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config['renaming']['val_cmo']:
                        th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config['abbrev']['val_arm_ini']:
                        th_list.append(html.Td(f'{float(content_td)/100:{config["formatting"]["val_arm_ini"]}}', colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config['abbrev']['val_ena_mw_m']:
                        if content_td != '':
                            th_list.append(html.Td(f'{float(content_td):{config["formatting"]["val_ena_mw_m"]}}', colSpan=f'{colspan_td}', className=f''))
                        else:
                            th_list.append(html.Td(f'{content_td.upper()}',  colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config['abbrev']['val_ena_mlt_m']:
                        th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config_carga['abbrev']['val_carga']:

                        if content_td != '':
                            th_list.append(html.Td(f'{float(content_td):{config_carga["formatting"]["val_carga"]}}'.replace(',','.'), colSpan=f'{colspan_td}', className=f''))
                        else:
                            th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config_gd['abbrev']['val_gd']:
                        if content_td != '':
                            th_list.append(html.Td(f'{content_td}'.replace(',', '.'), colSpan=f'{colspan_td}', className=f'' ) )
                        else:
                            th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))
                    elif table_type == config_gd['abbrev']['val_gd']:
                        if content_td != '':
                            th_list.append(html.Td(f'{content_td}'.replace(',', '.'), colSpan=f'{colspan_td}', className=f'' ) )
                        else:
                            th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))
                    else:
                        th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}', className=f''))

            tbody_list.append(html.Tr(th_list))

        tbody = [html.Tbody(tbody_list)]

        table = dbc.Table(
            id=f'id-`{id}',
            children=thead + tbody,
            class_name=f'{class_name} table-sm mx-0 px-0 text-center small justify-content-center',
            # striped=True
        )

        return table


    def table_unifield(self,
                       html_table: BeautifulSoup(),
                       table_type: str,
                       class_name: str,
                       title: str
                       ):

        config_carga = Config().config['carga']

        soup = BeautifulSoup(html_table, 'html.parser')

        thead = soup.thead
        tbody = soup.tbody

        tbody_list = []
        tr_thead = []

        # Create Thead
        flag = 0
        for tr in thead.find_all('tr'):
            th_list = []

            for th in tr.find_all('th'):
                try:
                    if th.text == '' and flag == 0:
                        content = title
                        flag = 1
                    else:
                        content = th.text
                except:
                    # content = ''
                    content = title

                try:
                    attrs = th.attrs
                    colspan = int(attrs['colspan'])
                except:
                    attrs = {'colspan': 0}
                    colspan = int(attrs['colspan'])


                th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}'))

            tr_thead.append(html.Tr(th_list))

        thead = [html.Thead(children=tr_thead, className='')]

        # Create Tbody
        for tr in tbody.find_all('tr'):
            th_list = []

            td_list = tr.find_all('td')
            len(td_list)
            for th in tr.find_all('th'):
                try:
                    content = th.text
                except:
                    content = ''

                # get colspan
                try:
                    attrs = th.attrs
                    colspan = int(attrs['colspan'])
                except:
                    attrs = {'colspan': 0}
                    colspan = int(attrs['colspan'])

                # get rowspan
                try:
                    attrs_row = th.attrs
                    rowspan = int(attrs_row['rowspan'])
                except:
                    attrs_row = {'rowspan': 1}
                    rowspan = int(attrs_row['rowspan'])

                # th_list.append(html.Th(f'{content.upper()}',))
                th_list.append(html.Th(f'{content.upper()}', colSpan=f'{colspan}', rowSpan=f'{rowspan}'))
            for td in td_list:
                try:
                    content_td = td.text
                except:
                    content_td = ''
                try:
                    attrs_td = td.attrs
                    colspan_td = int(attrs_td['colspan'])
                except:
                    attrs_td = {'colspan': 0}
                    colspan_td = int(attrs_td['colspan'])

                if table_type == config_carga['abbrev']['val_carga']:

                    if content_td != '':
                        th_list.append(
                            html.Td(
                                f'{float(content_td):{config_carga["formatting"]["val_carga"]}}'.replace(',', '.'),
                                colSpan=f'{colspan_td}',
                                className=f'')
                        )
                    else:
                        th_list.append(
                            html.Td(
                                f'{content_td}',
                                colSpan=f'{colspan_td}',
                                className=f''
                            )
                        )
                else:
                    th_list.append(html.Td(f'{content_td}', colSpan=f'{colspan_td}'))
                    # th_list.append(html.Td(f'{content_td.upper()}'.format(val_format), colSpan=f'{colspan_td}'))

            # float(content_td.replace('.', ','))
            #
            # float(content_td).format(val_format)

            tbody_list.append(html.Tr(th_list))

        # tbody = [html.Tbody()]
        tbody = [html.Tbody(tbody_list)]

        table = dbc.Table(
            id='id',
            children=thead + tbody,
            class_name=f'{class_name} table-sm mx-0 px-0 text-center small justify-content-center',
            # striped=True
        )

        return table