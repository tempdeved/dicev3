
import pandas as pd
from config.config import Config
from banco.dados import Dados
import os
import shutil

# config = Config().config
config = Config().config2
dados = Dados(config['ambiente'])

def dump_alunos():
    path = r'../dump_files/Aluno-2023-05-08 (1).xls'

    df_alunos = pd.read_excel(path)

    df_alunos = df_alunos.fillna('').copy()

    dados.insert_into_table(df=df_alunos, table_name='aluno')

    df_alunos_query = dados.query_table(table_name='aluno')

    # copia fotos de acordo com nome nos arquivos
    for x, row in df_alunos_query.iterrows():

        if os.path.isfile(f'images/{row["foto"]}'):

            # copiando foto
            shutil.copyfile(f'images/{row["foto"]}', f'../static/images/aluno/{row["id"]}.jpg')
            # shutil.copyfile(f'images/{row["foto"]}', f'../static/images/server/{row["id"]}.jpg')

            # atualizando na tabela
            dados.update_table(
                values={
                    'id': row["id"],
                    'foto': f'{row["id"]}.jpg'
                },
                table_name='aluno',
                pk_value=row["id"],
                pk_name='id'
            )

        else:
            print(f'Aluno não possui foto: {row["id"]} - {row["nome"]}')

def dum_horario():
    print('--- moc horarios')

    dia_semana = [
        'Segunda-feira'.upper(),
        'Quarta-feira'.upper(),

        'Segunda-feira'.upper(),
        'Quarta-feira'.upper(),

        'Segunda-feira'.upper(),
        'Quarta-feira'.upper(),

        'Segunda-feira'.upper(),
        'Quarta-feira'.upper(),

        'Segunda-feira'.upper(),
        'Quarta-feira'.upper(),

        #

        'Terça-feira'.upper(),
        'Quinta-feira'.upper(),

        'Terça-feira'.upper(),
        'Quinta-feira'.upper(),

        'Terça-feira'.upper(),
        'Quinta-feira'.upper(),

        'Terça-feira'.upper(),
        'Quinta-feira'.upper(),


    ]

    hora_inicio = [
        8,
        8,

        9,
        9,

        15,
        15,

        17,
        17,

        17,
        17,

        8,
        8,

        9,
        9,

        15,
        15,

        17,
        17,

    ]

    min_inicio = [
        0,
        0,

        40,
        40,

        30,
        30,

        10,
        10,

        30,
        30,

        0,
        0,

        40,
        40,

        30,
        30,

        10,
        10,

    ]

    hora_fim = [
        9,
        9,

        11,
        11,

        17,
        17,

        18,
        18,

        19,
        19,

        9,
        9,

        11,
        11,

        17,
        17,

        18,
        18,

    ]

    min_fim = [
        30,
        30,

        10,
        10,

        0,
        0,

        40,
        40,

        0,
        0,

        30,
        30,

        10,
        10,

        0,
        0,

        40,
        40,

    ]

    df_hr = pd.DataFrame(
        data={
            'dia_semana': dia_semana,
            'hora_inicio': hora_inicio,
            'min_inicio': min_inicio,
            'hora_fim': hora_fim,
            'min_fim': min_fim,
        }
    )

    dados.insert_into_table(df=df_hr, table_name='horario')

def dum_admin():

    config2 = Config().config2
    dados = Dados(config2['ambiente'])

    df_adm_user = pd.DataFrame(
        data={
            'email': ['ad'],
            'password': ['ad'],
            'status': ['Ativo'],
        }
    )

    dados.insert_into_table(df=df_adm_user, table_name='user')

    df_user = dados.query_table(
        table_name='user',
        filter_list=[
            {'op': 'eq', 'name': 'email', 'value': f'{df_adm_user["email"][0]}'},
        ]
    )

    df_func = pd.DataFrame(
        data={
            'email_func': [df_user["email"][0]],
            'nome_completo': ['administrador'],
            'tipo': ['Admin'],
        }
    )

    dados.insert_into_table(df=df_func, table_name='funcionario')



def migrate_user():

    """
    migrando usuários
    :return:
    """

    config = Config().config
    dados = Dados(config['ambiente'])

    config2 = Config().config2
    dados2 = Dados(config2['ambiente'])


    user1 = dados.query_table(table_name='user')
    user2 = dados2.query_table(table_name='user')

    user_filted = pd.concat(
        objs=[
            user2.drop(columns=['id']),
            user1.drop(columns=['id'])
        ],
        ignore_index=True
    )

    user_filted2 = user_filted[
        ~user_filted['email'].isin(user2['email'].to_list())
    ]

    dados2.insert_into_table(df=user_filted2, table_name='user')

    """
    migrando funcionarios
    """
    func1 = dados.query_table(table_name='funcionario')
    func2 = dados2.query_table(table_name='funcionario')

    func_filted = pd.concat(
        objs=[
            func2.drop(columns=['id']),
            func1.drop(columns=['id'])
        ],
        ignore_index=True
    )

    func_filted2 = func_filted[
        ~func_filted['email_func'].isin(func2['email_func'].to_list())
    ]

    dados2.insert_into_table(df=func_filted2, table_name='funcionario')


    """
    migrando turmas
    """

    turma1 = dados.query_table(table_name='turma')
    turma2 = dados2.query_table(table_name='turma')

    turma1['id_professor'] = turma1['id_professor'].astype(int)
    turma1['id_coordenador'] = turma1['id_coordenador'].astype(int)

    turma_filted = pd.concat(
        objs=[
            turma2.drop(columns=['id']),
            turma1.drop(columns=['id'])
        ],
        ignore_index=True
    )

    turma_filted2 = turma_filted[
        ~turma_filted['id_turma'].isin(turma2['id_turma'].to_list())
    ]

    dados2.insert_into_table(df=turma_filted2, table_name='turma')


    """
    migrando turma x aluno
    """

    turma_aluno1 = dados.query_table(table_name='turma_aluno')
    turma_aluno2 = dados2.query_table(table_name='turma_aluno')

    turma_aluno_filted = pd.concat(
        objs=[
            turma_aluno2.drop(columns=['id']),
            turma_aluno1.drop(columns=['id'])
        ],
        ignore_index=True
    )

    turma_aluno_filted2 = turma_aluno_filted[
        ~turma_aluno_filted['id_turma'].isin(turma_aluno2['id_turma'].to_list())
    ]

    dados2.insert_into_table(df=turma_aluno_filted2, table_name='turma_aluno')


    print('MIRAGACAO CONCLUIDA')


if __name__ == '__main__':
    print('INICIO')
    # dump_alunos()
    dum_horario()
    # dum_admin()
    # migrate_user()

