from PyQt5.QtCore import (
    QFile,
    QIODevice
)
import os.path
from .qlr_file import QlrFile

class LocalConfig:

    def __init__(self, settings):
        self.settings = settings
        self.reload()

    def reload(self):
        self.categories = []
        if self.settings.value('remember_settings'):
            self.local_qlr_filename = self.settings.value('custom_qlr_file')
            self.qlr_file = self.get_local_qlr_file()
            if self.qlr_file:
                self.categories = self.get_local_categories()

    def get_local_qlr_file(self):
        config = None
        if self.settings.value('remember_settings'):
            local_file_exists = os.path.exists(self.local_qlr_filename)
            if local_file_exists:
                config = self.read_local_qlr()

        if config:
            return QlrFile(config)
        else:
            return None

    def read_local_qlr(self):
        f = QFile(self.local_qlr_filename)
        f.open(QIODevice.ReadOnly)
        return f.readAll()

    def get_local_categories(self):
        local_categories = []
        groups_with_layers = self.qlr_file.get_groups_with_layers()
        for group in groups_with_layers:
            local_category = {
                'name': group['name'],
                'selectables': []
            }
            for layer in group['layers']:
                local_category['selectables'].append({
                    'type': 'layer',
                    'source': 'local',
                    'name': layer['name'],
                    'id': layer['id']
                    }
                )
            if len(local_category['selectables']) > 0:
                local_categories.append(local_category)
        return local_categories

    def get_categories(self):
        return self.categories

    def get_maplayer_node(self, id):
         return self.qlr_file.get_maplayer_node(id)



