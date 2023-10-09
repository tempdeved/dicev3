from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine, Column, Integer, Float, VARCHAR, DATETIME, ForeignKey, Text, UniqueConstraint,
    DATE, BOOLEAN, TEXT,ARRAY
)
from sqlalchemy.orm import relationship, backref
import sqlalchemy

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    # username = Column(VARCHAR(250), unique=True)
    email = Column(VARCHAR(250), unique=True)
    password = Column(VARCHAR(250))
    # nome_completo = Column(VARCHAR(250))
    # tipo = Column(VARCHAR(250))
    status = Column(VARCHAR(10))
    children = relationship('Funcionario')


    # __mapper_args__ = {
    #     'polymorphic_on': tipo
    # }

    #tipo: N - nutricionista, P - paciente, A - admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

class Aluno(Base):
    __tablename__ = "aluno"

    id = Column(Integer, primary_key=True)
    created_at = Column(DATE)
    nome = Column(VARCHAR(250))
    nome_do_meio = Column(VARCHAR(250))
    ultimo_nome = Column(VARCHAR(250))
    status = Column(VARCHAR(250))
    dat_nasc = Column(DATE)
    # mes_nascimento = Column(VARCHAR(250))
    cidade_nascimento = Column(VARCHAR(250))
    endereco = Column(VARCHAR(250))
    numero = Column(Integer)
    complemento = Column(VARCHAR(250))
    bairro = Column(VARCHAR(250))
    cidade = Column(VARCHAR(250))
    uf = Column(VARCHAR(250))
    cep = Column(VARCHAR(250))
    telefone1 = Column(VARCHAR(250))
    moradia = Column(VARCHAR(250))
    inicio = Column(DATE)
    n_irmaos = Column(Integer)
    retorno = Column(DATE)

    sexo = Column(VARCHAR(250))
    responsavel_financeiro = Column(VARCHAR(250))
    tel_responsavel_financeiro = Column(VARCHAR(250))
    responsavel_p_filhos = Column(VARCHAR(250))
    bairro_de_ida = Column(VARCHAR(250))
    bairro_de_volta = Column(VARCHAR(250))
    enviar_boleto = Column(BOOLEAN)
    gerar_taxa = Column(BOOLEAN)
    bolsista = Column(BOOLEAN)

    nome_pai = Column(VARCHAR(250))
    email_pai = Column(VARCHAR(250))
    celular_pai = Column(Integer)
    tel_trabalho_pai = Column(Integer)
    cpf_pai = Column(VARCHAR(250))
    profissao_pai = Column(VARCHAR(250))
    nome_mae = Column(VARCHAR(250))
    email_mae = Column(VARCHAR(250))
    celular_mae = Column(Integer)
    tel_trabalho_mae = Column(Integer)
    cpf_mae = Column(VARCHAR(250))
    profissao_mae = Column(VARCHAR(250))
    senha = Column(VARCHAR(250))
    foto = Column(VARCHAR(250))

class Funcionario(Base):
    __tablename__ = 'funcionario'

    id = Column(Integer, autoincrement=True, primary_key=True)
    # id_user = Column(ForeignKey('user.id'))
    email_func = Column(VARCHAR(250), ForeignKey(f'{User.__tablename__}.email'))
    # email_func = Column(VARCHAR(250))
    created_at = Column(DATE)
    nome_completo = Column(VARCHAR(250))
    tipo = Column(VARCHAR(250))
    # status = Column(VARCHAR(10))
    funcao = Column(VARCHAR(250))
    senha = Column(VARCHAR(250))
    telefone1 = Column(VARCHAR(250))
    telefone2 = Column(VARCHAR(250))
    dat_nasc = Column(DATE)
    cc = Column(VARCHAR(250))
    cart_profis = Column(VARCHAR(250))
    rg = Column(VARCHAR(250))
    endereco = Column(VARCHAR(250))
    numero = Column(Integer)
    complemento = Column(VARCHAR(250))
    bairro = Column(VARCHAR(250))
    cidade = Column(VARCHAR(250))
    uf = Column(VARCHAR(250))
    cep = Column(VARCHAR(250))

    foto = Column(VARCHAR(250))

class Horario(Base):
    __tablename__ = 'horario'

    id = Column(Integer, autoincrement=True, primary_key=True)
    dia_semana = Column(VARCHAR(250))
    hora_inicio = Column(VARCHAR(250))
    min_inicio = Column(VARCHAR(250))
    hora_fim = Column(VARCHAR(250))
    min_fim = Column(VARCHAR(250))

    children = relationship('Turma')


# class Turma(Base):
#     __tablename__ = 'turma'
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     id_turma = Column(Integer)
#     created_at = Column(DATE)
#
#     id_professor = Column(Integer, ForeignKey('user.id'))
#     id_coordenador = Column(Integer, ForeignKey('user.id'))
#     id_hr_turma = Column(Integer, ForeignKey('horario.id')) # menu check box
#     id_aluno = Column(Integer, ForeignKey('aluno.id'))
#
#     semestre = Column(VARCHAR(250))
#     numero_turma = Column(VARCHAR(250))
#     status = Column(VARCHAR(250))
#     escola = Column(VARCHAR(250))
#     observacao = Column(VARCHAR(250))
#     descricao = Column(VARCHAR(250))
#     nivel = Column(VARCHAR(250))
#     inicio = Column(DATE)
#     fim = Column(DATE)
#     map = Column(VARCHAR(250))
#     idioma = Column(VARCHAR(250))

class Turma(Base):
    __tablename__ = 'turma2'

    id = Column(Integer, autoincrement=True, primary_key=True)
    id_turma = Column(Integer)
    created_at = Column(DATE)

    id_professor = Column(TEXT)
    id_coordenador = Column(TEXT)
    id_hr_turma = Column(TEXT) # menu check box
    id_aluno = Column(TEXT)

    semestre = Column(VARCHAR(250))
    numero_turma = Column(VARCHAR(250))
    status = Column(VARCHAR(250))
    escola = Column(VARCHAR(250))
    observacao = Column(VARCHAR(250))
    descricao = Column(VARCHAR(250))
    nivel = Column(VARCHAR(250))
    inicio = Column(DATE)
    fim = Column(DATE)
    map = Column(VARCHAR(250))
    idioma = Column(VARCHAR(250))


class HistoricoAluno(Base):
    __tablename__ = 'historico_aluno'

    id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DATE)

    id_turma = Column(ForeignKey('turma2.id'))
    id_aluno = Column(ForeignKey('aluno.id'))

    numero_aulas = Column(Integer)
    numero_faltas = Column(Integer)
    research_01 = Column(Integer)
    organization_01 = Column(Integer)
    interest_01 = Column(Integer)
    group_activity_01 = Column(Integer)
    speaking_01 = Column(Integer)
    frequencia_of_01 = Column(Integer)
    listening_01 = Column(Integer)
    readind_inter_01 = Column(Integer)
    writing_process_01 = Column(Integer)


    descricao = Column(TEXT)

config = {
    'string_engine': r'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}',
    'credentials': dict(
        user='dice3',
        password='D1c9-3#ngl&6sh1a',
        host='3.80.101.37',
        port='3306',
        database='dicev3',
        # user='root',
        # password='',
        # host='127.0.0.1',
        # database='dicev3',
        # port='3306',
    ),
}

engine = create_engine(
    config["string_engine"].format(**config["credentials"]),
    pool_pre_ping=True, echo=False
)

Base.metadata.create_all(engine)
# # ------------------------------------------------------------