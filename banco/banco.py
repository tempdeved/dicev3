from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine


class Banco(object):

    def __init__(self, ambiente: dict):
        '''
        Creates map to a database.

        :param ambiente: Dict, Dicionario com credenciais de acesso ao banco.
        :returns None
        '''

        # Creating reflection
        Base = automap_base()
        try:
            self.engine = create_engine(
                url=ambiente['aws']['string_engine'].format(**ambiente['aws']['credentials']), echo=False, pool_pre_ping=True,
            )

            Base.prepare(self.engine, reflect=True)
            print("> Conectado via AWS")

        except:
            self.engine = create_engine(
                url=ambiente['nat']['string_engine'].format(**ambiente['nat']['credentials']), echo=False, pool_pre_ping=True,
            )

            Base.prepare(self.engine, reflect=True)
            print("> Conectado via NAT")

        # Creating names for tables
        self.tables = {v.__name__: v for v in Base.classes}

        try:
            Base.metadata.create_all(self.engine)
        except:
            raise (
                ConnectionError(
                    f'Erro na conexão com o banco de dados \n'
                    # f'{config["credenditals"]["db_bbce_ehub"]} - Host {config["credenditals"]["host"]}'
                )
            )

        return







# from sqlalchemy.ext.automap import automap_base
# # from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import (
#     Column, Integer, Float, CHAR, DATETIME, VARCHAR, Date,
#     create_engine, ForeignKey, PrimaryKeyConstraint,
#     BINARY,
# )
# from sqlalchemy.orm import declarative_base, relationship
#
# from sqlalchemy.schema import CreateColumn
#
# Base = declarative_base()
#
# # Curvas Forward
# class TipoCurva(Base):
#     __tablename__ = 'curva_forward_tipo'
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     # produto = Column(CHAR(length=100), )
#     # nom_curva = Column(CHAR(length=100), )
#     fonte = Column(CHAR(length=100), )
#     # tipo = Column(CHAR(length=100), )
#     desc = Column(CHAR(length=100), )
#
#
# class Submercado(Base):
#     __tablename__ = 'submercado'
#
#     id = Column(Integer, primary_key=True)
#     desc = Column(CHAR(length=15), )
#
#
# class CurvaForwardHist(Base):
#     __tablename__ = 'curva_forward_hist'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_tipo_curva = Column(Integer(), ForeignKey('curva_forward_tipo.id'))
#
#     dat_medicao = Column(DATETIME, index=True)
#     tipo_energia = Column(CHAR(length=100))
#     submercado = Column(CHAR(2), index=True)
#     preco_ref = Column(Float)
#     premio_energia = Column(Float)
#     premio_submercado = Column(Float)
#     preco_final = Column(Float)
#
#     dat_ref = Column(DATETIME, index=True)
#     created_at = Column(DATETIME, index=True)
#
#
# class CurvaForwardFormualrioHistorico(Base):
#     __tablename__ = 'curva_forward_formulario_hist'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_tipo_curva = Column(Integer)
#     desc_curva = Column(CHAR(length=30), )
#     dat_ini = Column(DATETIME, index=True,)
#     dat_fim = Column(DATETIME, index=True,)
#     se = Column(Float)
#     s = Column(Float)
#     ne = Column(Float)
#     n = Column(Float)
#     i0 = Column(Float)
#     i5 = Column(Float)
#     i1 = Column(Float)
#     cq5 = Column(Float)
#     dat_ref = Column(DATETIME, index=True,)
#     created_at = Column(DATETIME, index=True,)
#
#
# class FileCurvaForward(Base):
#     __tablename__ = 'curva_forward_file_uploaded'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tipo_file = Column(CHAR(length=15), )
#     path = Column(CHAR(length=255), )
#     id_tipo_curva = Column(Integer(), )
#     dat_ref = Column(DATETIME, index=True, )
#     created_at = Column(DATETIME, index=True,)
#
#
#
# # Inflação
# class TipoIndice(Base):
#     __tablename__ = 'inflacao_tipo'
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     nom_indicador = Column(CHAR(length=100), )
#     fonte = Column(CHAR(length=100), )
#     tipo = Column(CHAR(length=100), )
#
#
# class Indice(Base):
#     __tablename__ = 'inflacao'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_tipo_indice = Column(Integer(), ForeignKey('inflacao_tipo.id'), )
#     dat_medicao = Column(DATETIME, index=True, )
#     val_indice = Column(Float)
#     dat_ref = Column(DATETIME, index=True, )
#     created_at = Column(DATETIME, index=True,)
#
#
# # PLD
# class PLD(Base):
#     __tablename__ = 'pld'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     dat_medicao = Column(DATETIME, index=True)
#     cod_ssis = Column(Integer)
#     nom_ssis = Column(CHAR(5))
#     val_pld = Column(Float)
#
#
# # Feriados
# class Feriados(Base):
#     __tablename__ = 'feriados'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     data_feriado = Column(DATETIME, index=True)
#     descricao_feriado = Column(CHAR(50))
#
#
#
# # Portfolio
# class TipoOrganizacao(Base):
#     __tablename__ = 'tipo_organizacao'
#     # id = Column(Integer, primary_key=True, autoincrement=True)
#     cod_organizacao = Column(CHAR(2), primary_key=True)
#     nome_organizacao = Column(VARCHAR(100))
#
# class HistoricoBook(Base):
#     __tablename__ = 'historico_book'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     cod_cenario = Column(Integer, ForeignKey('curva_forward_tipo.id'))
#     data_referencia = Column(Date)
#     nome_organizacao = Column(VARCHAR(2))
#     data_faturamento = Column(Date)
#     data_apuracao = Column(Date)
#     nome_area_negocio = Column(VARCHAR(50))
#
#     id_submercado = Column(VARCHAR(2))
#     tipo_operacao = Column(VARCHAR(50))
#     tipo_energia = Column(VARCHAR(20))
#     tipo_preco = Column(VARCHAR(50))
#
#     exposicao_energetica_vigente_net = Column(Float)
#
#     total_financeiro_vigente_net = Column(Float)
#     total_financeiro_mercado_net = Column(Float)
#     total_financeiro_mtm_net = Column(Float)
#
#     total_financeiro_vigente_net_vpl = Column(Float)
#     total_financeiro_mercado_net_vpl = Column(Float)
#     total_financeiro_mtm_net_vpl = Column(Float)
#
#
# # B3
# class TaxasB3(Base):
#     __tablename__ = 'taxa_referencial'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_taxa_referencial = Column(Integer)
#     dias_corridos = Column(Integer)
#     val_indice = Column(Float)
#     dat_ref = Column(DATETIME)
#     created_at = Column(DATETIME)
#
#
# # Credito
#
# class GrupoEconomico(Base):
#     __tablename__ = 'grupo_economico'
#
#     id_grupo_economico = Column(Integer, primary_key=True, autoincrement=True)
#     grupo_economico = Column(VARCHAR(length=100))
#     tipo_grupo_economico = Column(VARCHAR(50))
#
# class Contraparte(Base):
#     __tablename__ = 'contraparte'
#
#     id_contraparte = Column(Integer, primary_key=True, autoincrement=True)
#     id_grupo_economico = Column(Integer, ForeignKey('grupo_economico.id_grupo_economico'), index=True)
#     razao_social = Column(VARCHAR(length=100), index=True)
#     tipo_contraparte = Column(VARCHAR(50))
#     txt_cnpj = Column(VARCHAR(length=18), index=True)
#
# class Credito(Base):
#     __tablename__ = 'credito_contraparte'
#
#     # Cadastro de contraparte e grupo economico
#     id_credito = Column(Integer, primary_key=True, autoincrement=True)
#     id_contraparte = Column(Integer, ForeignKey('contraparte.id_contraparte'), index=True)
#     id_grupo_economico = Column(Integer, ForeignKey('grupo_economico.id_grupo_economico'), index=True)
#
#     # Cadastro da linha temporal da revisao dos dados
#     data_referencia = Column(DATETIME, index=True)
#     id_comite_credito = Column(Integer, index=True)
#
#     # Dados
#     capital_social = Column(Float)
#     rating_calculado = Column(VARCHAR(length=10))
#     rating_aprovado = Column(VARCHAR(length=10))
#     limite_aprovado = Column(Float)
#     prob_default = Column(Float)
#
# class HistoricoContrapartes(Base):
#     __tablename__ = 'historico_contrapartes'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     nome_organizacao = Column(CHAR(10), ForeignKey('tipo_organizacao.cod_organizacao'))
#     nome_area_negocio = Column(CHAR(50))
#     cod_cenario = Column(Integer, ForeignKey('curva_forward_tipo.id'))
#     data_referencia = Column(DATETIME)
#     data_faturamento = Column(DATETIME)
#     data_apuracao = Column(DATETIME)
#     id_grupo_economico = Column(Integer, ForeignKey('grupo_economico.id_grupo_economico'))
#     nome_grupo_economico = Column(VARCHAR(200))
#
#     exposicao_energetica_vigente_net = Column(Float)
#
#     total_financeiro_vigente_net = Column(Float)
#     total_financeiro_mercado_net = Column(Float)
#     total_financeiro_mtm_net = Column(Float)
#
#     total_financeiro_vigente_net_vpl = Column(Float)
#     total_financeiro_mercado_net_vpl = Column(Float)
#     total_financeiro_mtm_net_vpl = Column(Float)
#
#
#
#
#
#
# # To create tables
# string_engine = r'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'
# #
# config = dict(
#     user='root',
#     password='VPuZKK4xh5#0',
#     host='portfolio-sp.c2p8zw3iinxp.sa-east-1.rds.amazonaws.com',
#     database='newcom_sp',
#     port='3306',
# )
#
# engine_db = create_engine(
#     url=string_engine.format(**config),
#     # url=config['databases']['string_engine'].format(**config['databases']['inflacao']),
#     pool_pre_ping=True, echo=False
# )
#
# try:
#     Base.metadata.create_all(engine_db)
# except:
#     engine = create_engine(config)
#     Base.metadata.create_all(engine_db)
#
