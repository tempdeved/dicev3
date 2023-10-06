import pandas as pd

class Conveter(object):

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
        df['% Flexibilidade Mensal (Mín)'] = df['% Flexibilidade Mensal (Mín)'].astype(dtype='float')
        df['fontes'] = df['Classe'].map(fontes, na_action='ignore')
        df['Data Base'] = pd.to_datetime(df['Data Base'], format='%d/%m/%Y')
        df['Início Contrato'] = pd.to_datetime(df['Início Contrato'], format='%d/%m/%Y')
        df['Fim Contrato'] = pd.to_datetime(df['Fim Contrato'], format='%d/%m/%Y')
        df['Data Acordo Comercial'] = pd.to_datetime(df['Data Acordo Comercial'], format='%d/%m/%Y')

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