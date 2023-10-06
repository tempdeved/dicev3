import os
import pandas as pd
import locale
from datetime import datetime

from parallel.parallel import worker
# from utils.glorian.glorian import Conveter
from glorian.processamento.portfolio.reajuste import ReajusteNewcom, ReajusteBBCE, SemReajuste

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class Convert(object):

    def __init__(self):

        ...

    def convert(self, df: pd.DataFrame) -> pd.DataFrame:

        fontes = {
            'CONV': 'Convencional',
            'I5': 'Incentivada 50%',
            'I100': 'Incentivada 100%',
            'I0': 'Incentivada 0%',
            'INE50': 'INE50',
            'CQ5': 'CQ5'
        }


        df['Início Fornecimento'] = pd.to_datetime(df['Início Fornecimento'], format='%d/%m/%Y')
        df['Final Fornecimento'] = pd.to_datetime(df['Final Fornecimento'], format='%d/%m/%Y')
        df['tipo_preco'] = df.apply(lambda x: 'Preço Fixo' if x['Unidade'] == 'MWh' else 'Spread', axis=1)
        df['% Flexibilidade Mensal (Mín)'] = df['% Flexibilidade Mensal (Mín)'].str.replace(',','.').astype(dtype='float')
        df['% Flexibilidade Mensal (Máx)'] = df['% Flexibilidade Mensal (Máx)'].str.replace(',','.').astype(dtype='float')
        df['fontes'] = df['Classe'].map(fontes, na_action='ignore')
        df['Data Base'] = pd.to_datetime(df['Data Base'], format='%d/%m/%Y')
        df['Início Contrato'] = pd.to_datetime(df['Início Contrato'], format='%d/%m/%Y')
        df['Fim Contrato'] = pd.to_datetime(df['Fim Contrato'], format='%d/%m/%Y')
        df['Data Acordo Comercial'] = pd.to_datetime(df['Data Acordo Comercial'], format='%d/%m/%Y')

        # fontes = {
        #     'CONV': 'Convencional',
        #     'I5': 'Incentivada 50%',
        #     'I100': 'Incentivada 100%',
        #     'I0': 'Incentivada 0%',
        #     'INE50': 'INE50',
        #     'CQ5': 'CQ5'
        # }
        #
        #
        # df['Início Fornecimento'] = pd.to_datetime(df['Início Fornecimento'], format='%d/%m/%Y')
        # df['Final Fornecimento'] = pd.to_datetime(df['Final Fornecimento'], format='%d/%m/%Y')
        # df['tipo_preco'] = df.apply(lambda x: 'Preço Fixo' if x['Unidade'] == 'MWh' else 'Spread', axis=1)
        # df['% Flexibilidade Mensal (Mín)'] = df['% Flexibilidade Mensal (Mín)'].astype(dtype='float')
        # df['fontes'] = df['Classe'].map(fontes, na_action='ignore')
        # df['Data Base'] = pd.to_datetime(df['Data Base'], format='%d/%m/%Y')
        # df['Início Contrato'] = pd.to_datetime(df['Início Contrato'], format='%d/%m/%Y')
        # df['Fim Contrato'] = pd.to_datetime(df['Fim Contrato'], format='%d/%m/%Y')
        # df['Data Acordo Comercial'] = pd.to_datetime(df['Data Acordo Comercial'], format='%d/%m/%Y')

        return df

    def convert_glorian_to_ri(self, df: pd.DataFrame ) -> pd.DataFrame:


        # Convertando dados coluna a coluna
        df_convertido = pd.DataFrame()

        df['dia'] = 1
        df_convertido['Mês de Apuração'] = pd.to_datetime(dict(year=df['Ano'], month=df['Mês'], day=df['dia']))
        df_convertido['Contraparte'] = df['Contraparte'].str[20:].str.strip()
        df_convertido['Contrato'] = df['Código']
        df_convertido['Suprimento'] = df.apply(
            func=lambda x: f'{x["Início Fornecimento"]:%d/%m/%Y} ~ {x["Final Fornecimento"]:%d/%m/%Y}',
            axis=1
        )
        df_convertido['Tipo Operação'] = df['Tipo']
        df_convertido['Tipo Prazo'] = df['Tipo.1']
        df_convertido['Negociação'] = df['Tipo.1']
        df_convertido['Produto'] = df.apply(
            func=lambda x: f'{x["Submercado"][0:2]} {x["Classe"][0:3]} {x["Início Fornecimento"]: %b/%y} - '
                           f'{x["Final Fornecimento"]: %b/%y} - {x["tipo_preco"]}'.upper(),
            axis=1
        )

        df_convertido['Submercado'] = df['Submercado']
        df_convertido['Fonte'] = df['fontes']
        df_convertido['Flex(%)'] = df.apply(
            func=lambda x: f'{x["% Flexibilidade Mensal (Mín)"]:.0f}% - {x["% Flexibilidade Mensal (Máx)"]:.0f}%',
            axis=1
        )
        df_convertido['Faturamento'] = ''
        df_convertido['Estado'] = ''
        df_convertido['MWh'] = df['Qtd vigente (MWh)']
        df_convertido['Flex Mensal(%)'] = ''
        df_convertido['Preço(R$)'] = df['Preço Vigente']
        df_convertido['Tipo Preço'] = df.apply(lambda x: 'FIXO' if x['Unidade'] == 'MWh' else 'SPREAD', axis=1)
        df_convertido['PLD'] = ''
        df_convertido['Zeragem'] = ''
        df_convertido['MW médio'] = df['Quantidade (Net)']
        df_convertido['Faturamento(R$)'] = df['Total Vigente (Net)']
        df_convertido['Liquidação(R$)'] = ''
        df_convertido['MtM'] = ''
        df_convertido['Cliente'] = ''
        df_convertido['Grupo de Empresa'] = ''
        df_convertido['Data Fechamento da Proposta'] = df['Data Acordo Comercial']
        df_convertido['Energia Recompra(MWh)'] = ''
        df_convertido['CP Auto'] = ''
        df_convertido['CNAE'] = ''
        df_convertido['SETOR'] = ''
        df_convertido['TIPO CONTRAPARTE'] = ''

        return df_convertido

    def execute(
            self,
            # path: str,
            file_name: pd.DataFrame(),
            path_ipca: str,
            path_export: str,
    ):

        """
        TODO Verificar locale pt-br funciona no AWS EB
        TODO Ver no glorian qual melhor campo para definir se a boleta foi preço fixo ou spread
        TODO Coluna Negociação precisa ser MESA/BBCE. Fazer baseado na coluna Tipo.1
        TODO Verificar se excel aceita coluna fonte/classe com nomes abreviados
        TODO Verificar se excel aceita coluna flex com formatação do conversor
        TODO Verificar se excel aceita coluna FATURAMENTO vazia
        TODO Verificar se excel aceita coluna Estado vazia
        TODO Verificar se excel aceita coluna Flex Mensal(%) com formatação do conversor
        """

        # path = r'C:\Users\ander\Downloads'
        # file_name = r'Portifólio_20230328163627988.csv'
        # path_ipca = r'C:\Users\ander\Downloads\inflacao.csv'
        # path_export = r'C:\Users\ander\Downloads'

        df_ipca = pd.read_csv(
            filepath_or_buffer=path_ipca,
            sep=';',
            decimal=',',
            encoding='ISO-8859-1'

        )

        df_ipca['val_indice_shifted'] = df_ipca['val_indice'].shift(1)
        df_ipca['val_inflacao_relativo'] = 1 - df_ipca['val_indice'] / df_ipca['val_indice_shifted']

        df_ipca['val_inflacao_acum'] = (df_ipca['val_inflacao_relativo'] + 1).cumprod()
        df_ipca['dat_medicao'] = pd.to_datetime(df_ipca['dat_medicao'], format='%d/%m/%Y')

        df = file_name
        #     pd.read_csv(
        #     filepath_or_buffer=os.path.join(path, file_name),
        #     sep=';',
        #     decimal=',',
        #     encoding='ISO-8859-1'
        # )

        # formatando colunas
        df = self.convert(df=df)
        # df = Conveter().convert(df=df)

        # estrutura de chain of responsability
        encadeamento_reajustes = ReajusteNewcom(
            next=ReajusteBBCE(
                next=SemReajuste(),
                inflacao=df_ipca,
            ),
            inflacao=df_ipca
        )


        # df = pd.concat([df, df, df, df, df, df], ignore_index=True)


        # df_bbce = df[df['Tipo.1'].isin(['VBBCE', 'CBBCE'])]
        # df_newcom = df[df['Tipo.1'].isin(['V_LEG', 'C_LEG'])]

        t = datetime.now()
        results = worker(func=encadeamento_reajustes.calcula_reajuste, iterables=[x for i, x in df.iterrows()])
        print(f'Total: {datetime.now() - t}')


        df_precos_atualizados = pd.concat(results, axis=1).T
        df_precos_atualizados.sort_values(by=['Código', 'Ano', 'Mês'], ascending=True, inplace=True)

        # Convertando dados coluna a coluna
        df_convertido = self.convert_glorian_to_ri(df=df)
        # df_convertido = Conveter().convert_glorian_to_ri(df=df)

        print(f'Total: {datetime.now() - t}')

        # exporting data
        df_convertido.to_csv(
            path_or_buf=os.path.join(path_export, f'portfolio-convertido-{datetime.now():%Y%m%d}.csv'),
            sep=';',
            decimal=',',
            index=False,
            encoding='ISO-8859-1'
        )

