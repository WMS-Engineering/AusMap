from PyQt5 import QtCore

from .ausmap_config import AusMapConfig
from .local_config import LocalConfig


class Config(QtCore.QObject):

    def __init__(self, settings):
        super(Config, self).__init__()
        self.settings = settings
        self.ausmap_config = AusMapConfig(settings)
        self.local_config = LocalConfig(settings)

    def load(self):
        self.local_config.load()
        self.ausmap_config.load()

        self.ausmap_groups_and_layers = self.ausmap_config.get_categories()
        self.local_groups_and_layers = self.local_config.get_categories()

        self.groups_and_layers = []
        self.groups_and_layers.append(self.ausmap_groups_and_layers)
        self.groups_and_layers.append(self.local_groups_and_layers)

    def get_groups_and_layers(self):
        return self.groups_and_layers

    def get_ausmap_maplayer_node(self, id):
        return self.ausmap_config.get_maplayer_node(id)

    def get_local_maplayer_node(self, id):
        return self.local_config.get_maplayer_node(id)
