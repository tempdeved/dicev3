
import pandas as pd
from config.config import Config
from banco.dados import Dados
import os
import shutil

def dump_alunos():
    path = r'../dump_files/Aluno-2023-05-08 (1).xls'
    config = Config().config
    dados = Dados(config['ambiente'])

    df_alunos = pd.read_excel(path)

    df_alunos = df_alunos.fillna('').copy()

    dados.insert_into_table(df=df_alunos, table_name='aluno')

    df_alunos_query = dados.query_table(table_name='aluno')

    # mover fotos
    for x, row in df_alunos_query.iterrows():

        if os.path.isfile(f'images/{row["foto"]}'):

            # copiando foto
            shutil.copyfile(f'images/{row["foto"]}', f'../static/images/aluno/{row["id"]}.jpg')

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


if __name__ == '__main__':
    dump_alunos()