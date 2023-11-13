import os
import pathlib
from omegaconf import DictConfig, OmegaConf


class Config(object):

    def __init__(self):

        b3 = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'acoes', 'b3.yaml'))
        tradingview = OmegaConf.load(file_=os.path.join(os.path.dirname(__file__), 'tradingview', 'tradingview.yaml'))

        self.config = OmegaConf.merge(b3, tradingview)
        self.config = OmegaConf.to_container(self.config)

