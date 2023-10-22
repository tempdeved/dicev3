import dash
from dash import html

page_name='error'
dash.register_page(__name__, path=f'/{page_name}')
# require_login(__name__)

def layout():
    result = html.Div(
        [
            html.H1('Error'),
            html.Div('content:'),
            html.Div(''),
        ]
    )

    return result