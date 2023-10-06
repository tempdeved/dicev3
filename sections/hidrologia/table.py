import datetime
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from utils.utils import Utils
import locale


class TableHidro(object):
    def __init__(self):
        ...

    def load(self, id, df: pd.DataFrame, table_css: str = '', value_format=',.0f', **kwargs):



        # build thead
        th_list = [html.Th('Sub')]

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
                    tr_list.append(html.Td(f'{v:{value_format}}'.replace(kwargs['replace'][0], kwargs['replace'][1])))
                except:
                    tr_list.append(html.Td(f'{v:{value_format}}'))

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
                       'justify-content-center ',

            children=table
        )

        return layout


