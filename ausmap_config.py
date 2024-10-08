import codecs
import json
import os.path
from urllib.request import urlopen

from PyQt5.QtCore import QFile, QIODevice, QObject, pyqtSignal
from PyQt5.QtWidgets import QAction
from qgis.core import QgsMessageLog

from .qlr_file import QlrFile


class AusMapConfig(QObject):
    kf_con_success = pyqtSignal()
    kf_con_error = pyqtSignal()
    kf_settings_warning = pyqtSignal()

    def __init__(self, settings):
        super(AusMapConfig, self).__init__()
        self.settings = settings

    def load(self):
        self.cached_ausmap_qlr_file = (
            self.settings.value("cache_path") + "ausmap_data.qlr"
        )

        self.qlr_file = self.get_qlr_file()
        self.categories = self.get_ausmap_categories()

    def get_categories(self):
        return self.categories

    def get_maplayer_node(self, id):
        return self.qlr_file.get_maplayer_node(id)

    def get_ausmap_categories(self):
        groups_with_layers = self.qlr_file.get_groups_with_layers()

        categories = []
        for group in groups_with_layers:
            category = {"name": group["name"], "selectables": []}
            for layer in group["layers"]:
                category["selectables"].append(
                    {
                        "type": "layer",
                        "source": "ausmap",
                        "name": layer["name"],
                        "id": layer["id"],
                    }
                )
            if len(category["selectables"]) > 0:
                categories.append(category)

        return categories

    def user_has_access(self, service_name):
        return service_name in self.allowed_kf_services["any_type"]["services"]

    def get_custom_categories(self):
        return []

    def get_qlr_file(self):
        config = None
        load_remote_config = True

        local_file_exists = os.path.exists(self.cached_ausmap_qlr_file)

        if load_remote_config:
            try:
                config = self.get_remote_qlr()
            except Exception as e:
                QgsMessageLog.logMessage(
                    "No contact to the configuration at "
                    + self.settings.value("ausmap_qlr")
                    + ". Exception: "
                    + str(e)
                )
                if not local_file_exists:
                    self.error_menu = QAction(
                        self.tr("No contact to AusMap"),
                        self.iface.mainWindow(),
                    )
                return
            self.write_cached_kf_qlr(config)
        if config:
            return QlrFile(config)
        else:
            return None

    def read_cached_kf_qlr(self):
        f = QFile(self.cached_ausmap_qlr_file)
        f.open(QIODevice.ReadOnly)
        return f.readAll()

    def get_remote_qlr(self):
        # response = urlopen(self.settings.value('ausmap_qlr'))
        # content = response.read()
        # content = unicode(content, 'utf-8')

        # Open local QLR file instead of reading the remote one
        with open(self.settings.value("ausmap_qlr"), "r") as reader:
            content = reader.read()

        return content

    def write_cached_kf_qlr(self, contents):
        """We only call this function IF we have a new version downloaded"""
        # Remove old versions file
        if os.path.exists(self.cached_ausmap_qlr_file):
            os.remove(self.cached_ausmap_qlr_file)

        # Write new version
        with codecs.open(self.cached_ausmap_qlr_file, "w", "utf-8") as f:
            f.write(contents)

    def debug_write_allowed_services(self):
        try:
            debug_filename = (
                self.settings.value("cache_path")
                + self.settings.value("username")
                + ".txt"
            )
            if os.path.exists(debug_filename):
                os.remove(debug_filename)
            with codecs.open(debug_filename, "w", "utf-8") as f:
                f.write(
                    json.dumps(
                        self.allowed_kf_services["any_type"]["services"],
                        indent=2,
                    )
                    .replace("[", "")
                    .replace("]", "")
                )
        except Exception as e:
            pass
