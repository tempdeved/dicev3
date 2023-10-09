from flask_login import current_user
from flask import session

from banco.dados import Dados
from config.config import Config

# from application import dados

config = Config().config
dados = Dados(config['ambiente'])


def user_is_authenticated():
    return current_user.is_authenticated

def verify_active_user(email):
    admin = dados.query_table(
        table_name='user',
        # operation='distinct',
        field_list=[
            {'name': 'email'},
            # {'name': 'tipo'},
            {'name': 'status'},
        ],
        filter_list=[
            # {'op': 'eq', 'name': 'tipo', 'value': 'Admin'},
            # {'op': 'eq', 'name': 'tipo', 'value': 'Gerente'},
            {'op': 'eq', 'name': 'email', 'value': email}
        ]
    )

    if admin['status'][0] == 'Ativo':
        return True
    else:
        return False
def is_professor_user(email):
    admin = dados.query_table(
        table_name='funcionario',
        # operation='distinct',
        field_list=[
            {'name': 'email_func'},
            {'name': 'tipo'},
        ],
        filter_list=[
            {'op': 'eq', 'name': 'email_func', 'value': email}
        ]
    )

    if admin['tipo'][0] == 'Professor':
        return True
    else:
        return False
def is_gerente_user(email):
    admin = dados.query_table(
        table_name='funcionario',
        # operation='distinct',
        field_list=[
            {'name': 'email_func'},
            {'name': 'tipo'},
        ],
        filter_list=[
            {'op': 'eq', 'name': 'email_func', 'value': email}
        ]
    )

    if admin['tipo'][0] == 'Gerente':
        return True
    else:
        return False
def is_admni_user(email):
    admin = dados.query_table(
        table_name='funcionario',
        # operation='distinct',
        field_list=[
            {'name': 'email_func'},
            {'name': 'tipo'},
        ],
        filter_list=[
            {'op': 'eq', 'name': 'email_func', 'value': email}
        ]
    )

    if admin['tipo'][0] == 'Admin':
        return True
    else:
        return False

def is_administrativo_user(email):
    admin = dados.query_table(
        table_name='funcionario',
        # operation='distinct',
        field_list=[
            {'name': 'email_func'},
            {'name': 'tipo'},
        ],
        filter_list=[
            {'op': 'eq', 'name': 'email_func', 'value': email}
        ]
    )

    if admin['tipo'][0] == 'Administrativo':
        return True
    else:
        return False


# def access_page():
# session["access_page"][session["_user_id"]][page_name]
#     return

# if __name__ == '__main__':
#     a = user_is_admin_or_gerente('b')
