
import dash
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
from pages.login import layout as login_layout
from flask_login import current_user
from utils.login_handler import require_login
from elements.titulo import Titulo


# page_name = __name__[6:].replace('.', '_')
# dash.register_page(__name__, path=f'/')
# require_login(__name__)

class SemPermissao(object):

    def rr(self):
        # if not current_user.is_authenticated:
        #     return login_layout()
        return Titulo().load(id='titulo-pagina', title_name='Usuário sem permissão'),

