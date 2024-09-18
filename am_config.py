import codecs
import os.path
from urllib.request import urlopen
from qgis.core import *
from PyQt5.QtCore import (
    QCoreApplication,
    QFileInfo,
    QFile,
    QUrl,
    QSettings,
    QTranslator,
    qVersion,
    QIODevice
)
from PyQt5.QtWidgets import QAction, QMenu, QPushButton

from PyQt5 import (
    QtCore,
    QtXml
)

import json

from .qlr_file import QlrFile
from .utils import log_message


class AmConfig(QtCore.QObject):
    kf_con_success = QtCore.pyqtSignal()
    kf_con_error = QtCore.pyqtSignal()
    kf_settings_warning = QtCore.pyqtSignal()

    def __init__(self, settings):
        super(AmConfig, self).__init__()
        self.settings = settings

    def load(self):
        self.cached_kf_qlr_filename = self.settings.value('cache_path') + 'ausmap_data.qlr'

        self.kf_qlr_file = self.get_kf_qlr_file()
        self.background_category, self.categories = self.get_kf_categories()

    def get_categories(self):
         return self.categories

    def get_background_category(self):
         return self.background_category

    def get_maplayer_node(self, id):
         return self.kf_qlr_file.get_maplayer_node(id)

    def get_kf_categories(self):
        kf_categories = []
        kf_background_category = None
        groups_with_layers = self.kf_qlr_file.get_groups_with_layers()
        for group in groups_with_layers:
            kf_category = {
                'name': group['name'],
                'selectables': []
            }
            for layer in group['layers']:
                kf_category['selectables'].append({
                    'type': 'layer',
                    'source': 'kf',
                    'name': layer['name'],
                    'id': layer['id']
                    }
                )
            if len(kf_category['selectables']) > 0:
                kf_categories.append(kf_category)
                if group['name'] == 'Baggrundskort':
                    kf_background_category = kf_category
        return kf_background_category, kf_categories

    def user_has_access(self, service_name):
        return service_name in self.allowed_kf_services['any_type']['services']

    def get_custom_categories(self):
        return []

    def get_kf_qlr_file(self):
        config = None
        load_remote_config = True

        local_file_exists = os.path.exists(self.cached_kf_qlr_filename)

        if load_remote_config:
            try:
                config = self.get_remote_kf_qlr()
            except Exception as e:
                log_message(u'No contact to the configuration at ' + self.settings.value('kf_qlr_url') + '. Exception: ' + str(e))
                if not local_file_exists:
                    self.error_menu = QAction(
                        self.tr('No contact to AusMap'),
                        self.iface.mainWindow()
                    )
                return
            self.write_cached_kf_qlr(config)
        if config:
            return QlrFile(config)
        else:
            return None

    def read_cached_kf_qlr(self):
        f = QFile(self.cached_kf_qlr_filename)
        f.open(QIODevice.ReadOnly)
        return f.readAll()

    def get_remote_kf_qlr(self):
        # response = urlopen(self.settings.value('kf_qlr_url'))
        # content = response.read()
        # content = unicode(content, 'utf-8')

        # Open local QLR file instead of reading the remote one
        with open(self.settings.value('kf_qlr_url'), 'r') as reader:
            content = reader.read()

        return content

    def write_cached_kf_qlr(self, contents):
        """We only call this function IF we have a new version downloaded"""
        # Remove old versions file
        if os.path.exists(self.cached_kf_qlr_filename):
            os.remove(self.cached_kf_qlr_filename)

        # Write new version
        with codecs.open(self.cached_kf_qlr_filename, 'w', 'utf-8') as f:
            f.write(contents)

    def debug_write_allowed_services(self):
        try:
            debug_filename = self.settings.value('cache_path') + self.settings.value('username') + '.txt'
            if os.path.exists(debug_filename):
                os.remove(debug_filename)
            with codecs.open(debug_filename, 'w', 'utf-8') as f:
                f.write(json.dumps(self.allowed_kf_services['any_type']['services'], indent=2).replace('[', '').replace(']', ''))
        except Exception as e:
            pass
