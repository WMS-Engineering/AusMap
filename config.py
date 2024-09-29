from .ausmap_config import AusMapConfig
from .local_config import LocalConfig
from PyQt5 import (
    QtCore
)

class Config(QtCore.QObject):

    kf_con_error = QtCore.pyqtSignal()
    kf_settings_warning = QtCore.pyqtSignal()

    def __init__(self, settings):
        super(Config, self).__init__()
        self.settings = settings
        self.ausmap_config = AusMapConfig(settings)
        self.ausmap_config.kf_con_error.connect(self.propagate_kf_con_error)
        self.ausmap_config.kf_settings_warning.connect(self.propagate_kf_settings_warning)

        self.local_config = LocalConfig(settings)

    def propagate_kf_settings_warning(self):
        self.kf_settings_warning.emit()

    def propagate_kf_con_error(self):
        self.kf_con_error.emit()

    def load(self):
        self.local_config.reload()
        self.ausmap_config.load()

        self.categories = []
        self.categories_list = []

        self.kf_categories = self.ausmap_config.get_categories()
        self.local_categories = self.local_config.get_categories()

        self.categories = self.kf_categories + self.local_categories

        self.categories_list.append(self.kf_categories)
        self.categories_list.append(self.local_categories)

    def get_category_lists(self):
        return self.categories_list

    def get_categories(self):
        return self.categories

    def get_kf_maplayer_node(self, id):
        return self.ausmap_config.get_maplayer_node(id)

    def get_local_maplayer_node(self, id):
        return self.local_config.get_maplayer_node(id)
