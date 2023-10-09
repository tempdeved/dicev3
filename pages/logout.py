import dash
from dash import html, dcc
from flask_login import logout_user, current_user
from flask import Flask, request, redirect, session, url_for
from elements.titulo import Titulo

dash.register_page(__name__)

def layout():
    if current_user.is_authenticated:
        session['email'] = 'logout'
        logout_user()

    # return redirect('/')
    return Titulo().load(id='titulo-pagina', title_name='Usuário desconectado'),
# html.Div(
#         [
#             html.Div(html.H2("Usuário desconectado")),
#             # dcc.Interval(id={'index': 'redirectLogin', 'type': 'redirect'}, n_intervals=0, interval=1 * 2000)
#         ]
#     )