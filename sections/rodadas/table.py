import datetime
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from utils.utils import Utils
import locale
from bs4 import BeautifulSoup

class TableRodada(object):
    def __init__(self):
        ...

    def load(self, id,
             df: pd.DataFrame,
             table_css: str = '',
             value_format=',.0f',
             tittle='Defalt table name',
             **kwargs):



        # build thead
        th_list = [html.Th(tittle)]
        # th_list = [html.Th('Sub')]

        for col in df.columns:

            if type(col) is datetime.date:
                th_list.append(html.Th(f'{col:%d-%m-%y}'))
            else:
                th_list.append(html.Th(f'{col.upper()}'))

        thead = [html.Thead(html.Tr(children=th_list), className='')]

        # build tbody
        tbody_list = list()
        for i, row in df.iterrows():
            tr_list = list()
            tr_list.append(html.Th(i))

            for v in row.values:
                try:
                    tr_list.append(html.Td(f'{v}'.replace(kwargs['replace'][1], kwargs['replace'][0])))
                    # tr_list.append(html.Td(f'{v:{value_format}}'.replace(kwargs['replace'][1], kwargs['replace'][0])))
                except:
                    tr_list.append(html.Td(f'{v}'))
                    # tr_list.append(html.Td(f'{v:{value_format}}'))

            tbody_list.append(html.Tr(tr_list))

        tbody = [html.Tbody(tbody_list)]

        table = dbc.Table(
            id=id,
            children=thead + tbody,
            class_name=table_css
        )

        layout = dbc.Row(
            id=f'row-table-section-{id}',
            class_name='mx-0 px-0 text-end wh-100 '
                       'justify-content-center '
                       'table-sm col-lg-3 col-md-6 col-sm-12',

            children=table
        )

        return layout

    def curto_prazo(self, id: str,
                    df1: pd.DataFrame,
                    df2: pd.DataFrame,
                    table_css: str = '',
                    val_format_mwmed='{:,.0f}',
                    val_format_mlt='{:.0%}',
                    tittle='Defalt table name',
                    **kwargs):

        # val_format_mwmed=',.0f',
        # val_format_mlt=',.0f',


        # build thead
        th_list = [html.Th(tittle, rowSpan=2, className='align-middle text-center')]
        # th_list = [html.Th('Sub')]
        th_multi_index = []

        for col in df1.columns:
            if type(col) is datetime.date:
                th_list.append(html.Th(f'{col:%d-%m-%y}', className='text-center', colSpan=2))
            else:
                th_list.append(html.Th(f'{col.upper()}', className='text-center', colSpan=2))

        for col in df1.columns:
            if type(col) is datetime.date:
                th_multi_index.append(html.Th(f'MWMED',))
                th_multi_index.append(html.Th(f'MLT',))
            else:
                th_multi_index.append(html.Th(f'MWMED',))
                th_multi_index.append(html.Th(f'MLT',))

        thead = [html.Thead(children=[
            html.Tr(children=th_list),
            # html.Tr(children=th_multi_index)
        ])]

        count = 0

        # build tbody
        tbody_list = list()
        for i, row in df1.iterrows():

            tr_list = list()
            tr_list.append(html.Th(i, className='align-middle text-center'))

            semana_ativa_mlt_df = df2.values[count]
            count = count + 1

            semana_ativa_mwmed_df = row.values

            for v in range(0, len(semana_ativa_mwmed_df)):
                try:
                    tr_list.append(html.Td(f'{semana_ativa_mwmed_df[v]}'.replace(kwargs['replace'][1], kwargs['replace'][0])))
                    tr_list.append(html.Td(f'{semana_ativa_mlt_df[v]}'.replace(kwargs['replace'][1], kwargs['replace'][0])))
                except:
                    tr_list.append(html.Td(f'{semana_ativa_mwmed_df[v]}'))
                    tr_list.append(html.Td(f'{semana_ativa_mlt_df[v]}'))

            tbody_list.append(html.Tr(tr_list))

        tbody = [html.Tbody(tbody_list)]

        table = dbc.Table(
            id=id,
            children=thead + tbody,
            class_name=table_css
        )

        layout = dbc.Col(
            id=f'row-table-section-{id}',
            # class_name='mx-0 px-0 text-end wh-100 '
            #            'justify-content-center '
            #             'table-sm col-lg-3 col-md-6 col-sm-12',

            children=table
        )

        return layout

    def generic_table(self,
                      html_table: BeautifulSoup(),
                      table_type: str,
                      val_format: str,
                      class_name: str,
                      title: str
                      ):

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

                    if table_type == 'preco':
                        if content_td != '' and float(content_td) > 70:
                            th_list.append(html.Td(f'{float(content_td):{val_format}}',
                                                   colSpan=f'{colspan_td}',
                                                   className=f'text-success'))
                        elif content_td != '':
                            th_list.append(html.Td(f'{float(content_td):{val_format}}',
                                                   colSpan=f'{colspan_td}', #className=f'text-success'
                                                   ))
                        else:
                            th_list.append(html.Td(f'{content_td.upper()}',
                                                   colSpan=f'{colspan_td}',
                                                   className=f''))
                    elif table_type == 'cmo':
                        # if content_td != '' and float(content_td) > 70:
                        #     th_list.append(html.Td(f'{float(content_td):{val_format}}',
                        #                            colSpan=f'{colspan_td}',
                        #                            className=f'text-success'))
                        if content_td != '':
                            th_list.append(html.Td(f'{float(content_td):{val_format}}',
                                                   colSpan=f'{colspan_td}', #className=f'text-success'
                                                   ))
                        else:
                            th_list.append(html.Td(f'{content_td.upper()}',
                                                   colSpan=f'{colspan_td}',
                                                   className=f''))
                    elif table_type == 'arm_ini':
                        if content_td != '' and float(content_td[:-1]) < 50:
                            th_list.append(html.Td(f'{float(content_td)/100:{val_format}}'.replace(',', '.'),
                                                   colSpan=f'{colspan_td}',
                                                   className=f'text-danger'))
                        elif content_td != '' and float(content_td[:-1]) < 60:
                            th_list.append(html.Td(f'{float(content_td)/100:{val_format}}'.replace(',', '.'),
                                                   colSpan=f'{colspan_td}',
                                                   className=f'text-warning'))
                        elif content_td == '':
                            th_list.append(html.Td(f'{content_td}',
                                                   colSpan=f'{colspan_td}', #className=f'text-success'
                                                   ))
                        else:
                            th_list.append(html.Td(f'{float(content_td)/100:{val_format}}'.replace(',', '.'),
                                                   colSpan=f'{colspan_td}',
                                                   className=f'text-success'))
                    elif table_type == 'ena':
                        if content_td != '' and float(content_td):
                            th_list.append(html.Td(f'{float(content_td):{val_format}}'.replace(',', '.'),
                                                   colSpan=f'{colspan_td}'))
                        elif content_td != '':
                            th_list.append(html.Td(f'{float(content_td)}',
                                                   colSpan=f'{colspan_td}', #className=f'text-success'
                                                   ))
                        else:
                            th_list.append(html.Td(f'{content_td.upper()}',
                                                   colSpan=f'{colspan_td}'))
                    elif table_type == 'mlt':
                        try:
                            th_list.append(html.Td(f'{float(content_td)/100:{val_format}}',
                                                   colSpan=f'{colspan_td}'))
                        except:
                            th_list.append(html.Td(f'{content_td.upper()}',
                                                   colSpan=f'{colspan_td}'))
                    else:
                        # content_td
                        th_list.append(html.Td(f'{content_td.upper()}'.format(val_format),
                                               colSpan=f'{colspan_td}'))

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

    def table_unifield(self,
                      html_table: BeautifulSoup(),
                      table_type: str,
                      val_format: str,
                      class_name: str,
                      title: str
                      ):

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

                if table_type == 'preco':
                    if content_td != '' and float(content_td) > 70:
                        th_list.append(html.Td(f'{float(content_td):{val_format}}',
                                               colSpan=f'{colspan_td}',
                                               className=f'text-success'))
                    elif content_td != '':
                        th_list.append(html.Td(f'{float(content_td):{val_format}}',
                                               colSpan=f'{colspan_td}', #className=f'text-success'
                                               ))
                    else:
                        th_list.append(html.Td(f'{content_td.upper()}',
                                               colSpan=f'{colspan_td}',
                                               className=f''))
                elif table_type == 'cmo':
                    # if content_td != '' and float(content_td) > 70:
                    #     th_list.append(html.Td(f'{float(content_td):{val_format}}',
                    #                            colSpan=f'{colspan_td}',
                    #                            className=f'text-success'))
                    if content_td != '':
                        th_list.append(html.Td(f'{float(content_td):{val_format}}',
                                               colSpan=f'{colspan_td}', #className=f'text-success'
                                               ))
                    else:
                        th_list.append(html.Td(f'{content_td.upper()}',
                                               colSpan=f'{colspan_td}',
                                               className=f''))
                elif table_type == 'arm_ini':
                    if content_td != '' and float(content_td[:-1]) < 50:
                        th_list.append(html.Td(f'{float(content_td)/100:{val_format}}'.replace(',', '.'),
                                               colSpan=f'{colspan_td}',
                                               className=f'text-danger'))
                    elif content_td != '' and float(content_td[:-1]) < 60:
                        th_list.append(html.Td(f'{float(content_td)/100:{val_format}}'.replace(',', '.'),
                                               colSpan=f'{colspan_td}',
                                               className=f'text-warning'))
                    elif content_td == '':
                        th_list.append(html.Td(f'{content_td}',
                                               colSpan=f'{colspan_td}', #className=f'text-success'
                                               ))
                    else:
                        th_list.append(html.Td(f'{float(content_td)/100:{val_format}}'.replace(',', '.'),
                                               colSpan=f'{colspan_td}',
                                               className=f'text-success'))
                elif table_type == 'ena':
                    if content_td != '' and float(content_td):
                        th_list.append(html.Td(f'{float(content_td):{val_format}}'.replace(',', '.'),
                                               colSpan=f'{colspan_td}'))
                    elif content_td != '':
                        th_list.append(html.Td(f'{float(content_td)}',
                                               colSpan=f'{colspan_td}', #className=f'text-success'
                                               ))
                    else:
                        th_list.append(html.Td(f'{content_td.upper()}',
                                               colSpan=f'{colspan_td}'))
                elif table_type == 'mlt':
                    try:
                        th_list.append(html.Td(f'{float(content_td)/100:{val_format}}',
                                               colSpan=f'{colspan_td}'))
                    except:
                        th_list.append(html.Td(f'{content_td.upper()}',
                                               colSpan=f'{colspan_td}'))
                else:
                    th_list.append(html.Td(f'{content_td.upper()}'.format(val_format), colSpan=f'{colspan_td}'))

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


