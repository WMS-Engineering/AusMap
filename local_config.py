import os
from PyQt5.QtCore import (
    QFile,
    QIODevice
)
from .qlr_file import QlrFile

class LocalConfig:
    """
    Handles the layers in the user's custom QLR file if it is provided in the plugin settings
    """
    def __init__(self, settings):
        self.settings = settings
        self.reload()

    def reload(self):
        self.categories = []
        self.local_qlr_file = self.settings.value('custom_qlr_file')
        if self.local_qlr_file:
            self.qlr_file = self.get_local_qlr_file()
            if self.qlr_file:
                self.categories = self.get_local_categories()

    def get_local_qlr_file(self):
        config = None
        if os.path.exists(self.local_qlr_file):
            config = self.read_local_qlr()
        if config:
            return QlrFile(config)
        else:
            return None

    def read_local_qlr(self):
        f = QFile(self.local_qlr_file)
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



