import pandas as pd
import datetime
import logging
from sqlalchemy import (create_engine, column, delete, select, distinct, func)
from sqlalchemy.orm.session import Session
from sqlalchemy import insert, update
from omegaconf import OmegaConf


from banco.banco import *
from banco.builders import *
from config.config import Config


class Dados(object):

    # def __init__(self, string_engine: str, credentials: dict):
    def __init__(self, ambiente: dict):
        '''
        Inicialização dos Bancos de Dados.

        :param ambiente: Dict, Dados de credenciais e string engine para banco de dados.
        '''

        banco = Banco(ambiente)

        self.engine = banco.engine

        self.tables = banco.tables

        # self.engine = create_engine(string_engine.format(**credentials), echo=False)
        #
        # self.tables = dict(
        #     submercado=Submercado,
        #     tipo_curva=TipoCurva,
        #     curva_forward_hist=CurvaForwardHist,
        #     portfolio=HistoricoBook,
        #     feriados=Feriados,
        #     taxas_b3=TaxasB3,
        #     pld=PLD,
        #     contraparte=Contraparte,
        #     grupo_economico=GrupoEconomico,
        #     credito=Credito,
        #     exposicao_contraparte=HistoricoContrapartes
        # )

        self.OPERATIONS = {
            'eq': GenericOperation(),
            'lt': GenericOperation(),
            'le': GenericOperation(),
            'gt': GenericOperation(),
            'ge': GenericOperation(),
            'in': In_()
        }


        # try:
        #     Base.metadata.create_all(self.engine)
        # except:
        #     raise (
        #         ConnectionError(
        #             f'Erro na conexão com o banco de dados \n'
        #             # f'{config["credenditals"]["db_bbce_ehub"]} - Host {config["credenditals"]["host"]}'
        #         )
        #     )
        ...

    def query_table(self, table_name: str, unique: bool=False, **kwargs) -> pd.DataFrame:
        """"

        **kwargs:
            operation: Operação distinct ou delete. Para SELECT deixar não colocar parametro

            filter_list: lista de campos que devem aparecer na query [{'name': 'dat_ref'}]

            field_list: lista filtros da query [{'op': 'eq', 'name': 'id_tipo_curva', 'value': id_curve}]


        """
        table = self.tables[table_name]

        print(f'Query na tabela: {table_name.upper()}')

        if 'field_list' in kwargs:
            print(f'Campos de {table_name.upper()} selecionados: {kwargs["field_list"]}')

            fields = [getattr(table, x['name']) for x in kwargs['field_list']]
        else:
            print(f'Campos de {table_name.upper()} selecionados: * (todos)')
            fields = [table]

        # selecting data to database
        with Session(bind=self.engine) as session:

            query = session.query(*fields)

            if 'filter_list' in kwargs.keys():

                print(f'Filtros de aplicados na query: {kwargs["filter_list"]}')

                for filter in kwargs['filter_list']:
                    query = self.OPERATIONS[filter['op']].build(table=table, filter=filter, query=query)

            try:
                if 'operation' in kwargs.keys():
                    print(f'Operacao {kwargs["operation"].upper()} na tabela: {table_name.upper()}')

                    attr = getattr(query, kwargs['operation'])
                    query = getattr(query, attr.__name__)()

                print(f'Operacao SELECT na tabea: {table_name.upper()}')

                df = pd.read_sql(sql=query.statement, con=session.bind)
                print(f'Registros de: {table_name} selecionados. Total de registros: {df.shape[0]}')


            except Exception as error:

                session.rollback()
                print(f'Operação de insert falhou')
                raise error

            return pd.DataFrame(df)

    def insert_into_table(self, df: pd.DataFrame, table_name: str) -> None:

        print(f'Inserindo dados: {table_name.upper()}')

        table = self.tables[table_name]
        # data_to_insert = [table(**record) for record in df.to_dict(orient='records')]

        # Commiting data to database
        with Session(bind=self.engine) as session:
            d = datetime.datetime.now()
            # session.bulk_save_objects(objects=data_to_insert)
            # session.bulk_insert_mappings(mapper=table, mappings=df.to_dict(orient='records'))
            session.execute(statement=insert(table), params=df.to_dict(orient='records'))
            # print((datetime.datetime.now() - d))

            try:
                session.commit()
                print(
                    f'Dados inseridos corretamente: {table_name.upper()} em : '
                    f'{(datetime.datetime.now() - d).total_seconds():.2f} s'
                )
                session.close()

            except Exception as error:
                session.rollback()
                print(f'Operação de insert falhou: erro: {error}')
                raise error

    def remove_from_table(self, table_name: str, **kwargs) -> pd.DataFrame:

        print(f'Deletando dados de: {table_name.upper()}')

        table = self.tables[table_name]

        # selecting data to database
        with Session(bind=self.engine) as session:

            query = session.query(table)

            if 'filter_list' in kwargs.keys():
                for filter in kwargs['filter_list']:
                    query = self.OPERATIONS[filter['op']].build(table=table, filter=filter, query=query)


            # Adding delete parameter
            query = query.delete()

            try:
                session.commit()
                print(f'Dados deletados')

            except Exception as error:

                session.rollback()
                print(f'Operação de insert falhou')
                raise error


    def update_table(self, values: dict, table_name: str, pk_value, pk_name) -> None:

        # operation_list = list()
        # [operation_list.append(TradesEhub(**row.to_dict())) for i, row in df_trades.iterrows()]

        table = self.tables[table_name]

        with Session(bind=self.engine) as session:

            up = update(table)

            up = up.values(
               values
            )
            up = up.where(
                getattr(table, pk_name) == pk_value
            )

            # from sqlalchemy import inspect
            # insp = inspect(self.engine)
            # insp.get_table_names()
            # a = insp.get_columns(table_name='funcionario')

            try:
                session.execute(up)
                session.commit()
                print(f'Realizado update {pk_value}')

            except Exception as err:
                session.rollback()
                print(f'Erro no update do Produto {pk_value}')
                print(f'Tabela: {table.__table__}')
                print(f'{err}')







