
import pandas as pd
from config.config import Config
from banco.dados import Dados


def dump_alunos():
    path = r'../dump_files/Aluno-2023-05-08 (1).xls'
    config = Config().config
    dados = Dados(config['ambiente'])

    df_alunos = pd.read_excel(path)

    df_alunos.fillna('', inplace=True)

    dados.insert_into_table(df=df_alunos, table_name='aluno')

if __name__ == '__main__':
    dump_alunos()