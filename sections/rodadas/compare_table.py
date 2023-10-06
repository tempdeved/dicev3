import dash
import dash_bootstrap_components as dbc
import pandas as pd
from utils.utils import Utils

class TableSection(object):
    def __init__(self):
        ...


    def load(self, id, df:pd.DataFrame, table_css:str=''):

        formatted_table = Utils().convert_to_html_table(df=df, th_css='thead thead-dark', tbody_css='')

        layout = dbc.Row(
            id=f'row-table-section-{id}',
            class_name='px-2 overflow-auto',
            children=[
                dbc.Table(
                    id=f'table-section-{id}',
                    class_name=table_css,
                    children=[formatted_table['thead'], formatted_table['tbody']],
                    bordered=False,
                    hover=True,
                    striped=True,
                    color='secondary'
                )
            ]
        )

        return layout