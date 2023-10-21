import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True)


menu = ['test1', 'test2','test1', 'test2','test1', 'test2','test1', 'test2','test1', 'test2',]

"""
<div class="topnav" id="myTopnav">
  <a href="#home" class="active">Home</a>
  <a href="#news">News</a>
  <a href="#contact">Contact</a>
  <a href="#about">About</a>
  <a href="javascript:void(0);" class="icon" onclick="myFunction()">
    <i class="fa fa-bars"></i>
  </a>
</div>
"""

app.layout = html.Div([

    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    ),

    html.Div(
        id='myTopnav',
        className='topnav',
        children=[
            dbc.Row(
                children=[
                    dcc.Link('Edson', href='/test1'),
                    dcc.Link('Edson2', href='/test2'),
                    dcc.Link(
                        children=[
                            html.I(className='fa fa-bars')
                        ],
                        href='javascript:void(0);',
                        # href='',
                        className='icon',
                    ),
                    html.A(
                        children=[
                            html.I(className='fa fa-bars')
                        ],
                        href='javascript:void(0);',
                        role='myFunction()',
                        # href='',
                        className='icon',
                    ),
                    ]
            ),
            ]
    ),

    html.Div([
        html.Div(
            dcc.Link(f"{page}", href=page)
        ) for page in menu
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run()