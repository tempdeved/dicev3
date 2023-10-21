import os
import pathlib
from omegaconf import DictConfig, OmegaConf


class Config(object):

    def __init__(self):

        database_config = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'database', 'dice.yaml'))
        # layout_config = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'layout', 'layout.yaml'))
        secret = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'auth', '.secret'))

        self.config = OmegaConf.merge(database_config, secret)
        self.config = OmegaConf.to_container(self.config)

