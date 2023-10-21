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
                url=ambiente['aws']['string_engine'].format(**ambiente['aws']['credentials']),
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600,
            )

            Base.prepare(self.engine, reflect=True)
            print("> Conectado via AWS")

        except:
            self.engine = create_engine(
                url=ambiente['nat']['string_engine'].format(**ambiente['nat']['credentials']),
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600,
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
