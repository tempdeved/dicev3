
import pandas as pd
from config.config import Config
from banco.dados import Dados
import os
import shutil

config = Config().config
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


if __name__ == '__main__':
    dump_alunos()
    dum_horario()