import os
import pathlib
from omegaconf import DictConfig, OmegaConf


class Config(object):

    def __init__(self):

        database_config = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'database', 'dice.yaml'))
        cidades_brasil = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'brasil', 'cidades_brasil.yaml'))
        # layout_config = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'layout', 'layout.yaml'))
        secret = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'auth', '.secret'))
        pages = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'pages', 'relatorio_simples.yaml'))

        self.config = OmegaConf.merge(
            database_config,
            secret,
            cidades_brasil,
            pages,
        )
        self.config = OmegaConf.to_container(self.config)

