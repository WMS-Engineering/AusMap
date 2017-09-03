from kf_config import KfConfig
from local_config import LocalConfig
from PyQt4 import (
    QtCore
)

class Config(QtCore.QObject):

    kf_con_error = QtCore.pyqtSignal()
    kf_settings_warning = QtCore.pyqtSignal()
            
    def __init__(self, settings):
        super(Config, self).__init__()
        self.settings = settings
        self.kf_config = KfConfig(settings)
        self.kf_config.kf_con_error.connect(self.propagate_kf_con_error)
        self.kf_config.kf_settings_warning.connect(self.propagate_kf_settings_warning)

        self.local_config = LocalConfig(settings)

    def propagate_kf_settings_warning(self):
        self.kf_settings_warning.emit()
        
    def propagate_kf_con_error(self):
        self.kf_con_error.emit()
        
    def load(self):
        
        self.kf_config.load()

        self.categories = []
        self.categories_list = []
        if self.settings.value('use_custom_qlr_file') and self.settings.value('kf_only_background'):
            self.kf_categories = []
            background_category = self.kf_config.get_background_category()
            if background_category:
                self.kf_categories.append(background_category)
        else:
            self.kf_categories = self.kf_config.get_categories()
        self.local_categories = self.local_config.get_categories()
        
        self.categories = self.kf_categories + self.local_categories
        
        self.categories_list.append(self.kf_categories)
        self.categories_list.append(self.local_categories)

    def get_category_lists(self):
        return self.categories_list
    
    def get_categories(self):
        return self.categories

    def get_kf_maplayer_node(self, id):
        return self.kf_config.get_maplayer_node(id)
    
    def get_local_maplayer_node(self, id):
        return self.local_config.get_maplayer_node(id)
