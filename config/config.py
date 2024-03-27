import os
import pathlib
from omegaconf import DictConfig, OmegaConf


class Config(object):

    def __init__(self):

        database_config = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'database', 'dice.yaml'))
        database_config2 = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'database', 'dice2.yaml'))
        cidades_brasil = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'brasil', 'cidades_brasil.yaml'))
        home_config = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'layout', 'home.yaml'))
        secret = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'auth', '.secret'))
        pages = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'pages', 'relatorio_simples.yaml'))
        relatorio_etiqueta_alunos = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'pages', 'relatorio_etiqueta_alunos.yaml'))
        relatorio_telefone_turma = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'pages', 'relatorio_telefone_turma.yaml'))
        relatorio_turma_horario = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'pages', 'relatorio_turma_horario.yaml'))
        lancar_nota_turma = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'pages', 'lancar_nota_turma.yaml'))

        self.config = OmegaConf.merge(
            database_config,
            secret,
            cidades_brasil,
            pages,
            relatorio_etiqueta_alunos,
            relatorio_telefone_turma,
            relatorio_turma_horario,
            lancar_nota_turma,
            home_config,
        )
        self.config = OmegaConf.to_container(self.config)

        self.config2 = OmegaConf.merge(
            database_config2
        )
        self.config2 = OmegaConf.to_container(self.config2)

