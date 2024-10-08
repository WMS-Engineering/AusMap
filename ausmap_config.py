import codecs
import json
import os.path
from datetime import datetime
from urllib.request import urlopen

from PyQt5.QtCore import QFile, QIODevice, QObject, pyqtSignal
from qgis.core import Qgis, QgsMessageLog

from .constants import FILE_MAX_AGE
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

    def get_qlr_file(self):
        local_file_exists = os.path.exists(self.cached_ausmap_qlr_file)
        try:
            if local_file_exists:

                local_file_time = datetime.fromtimestamp(
                    os.path.getmtime(self.cached_ausmap_qlr_file)
                )
                use_local = local_file_time > datetime.now() - FILE_MAX_AGE
                if use_local:
                    # Skip requesting remote qlr
                    return self.get_cached_qlr()

            # Fetch remote QLR if local QLR is outdated or missing
            remote_ausmap_qlr = self.get_remote_qlr()
            self.write_local_qlr(remote_ausmap_qlr)

            return QlrFile(remote_ausmap_qlr)

        except Exception as error:
            QgsMessageLog.logMessage(
                f"An unexpected error occurred while fetching QLR file: {str(error)}",
                level=Qgis.Critical,
            )

    def get_cached_qlr(self):
        f = QFile(self.cached_ausmap_qlr_file)
        f.open(QIODevice.ReadOnly)
        content = f.readAll()
        return QlrFile(content)

    def get_remote_qlr(self):
        response = urlopen(self.settings.value("ausmap_qlr"))
        content = response.read().decode("utf-8")
        return content

    def write_local_qlr(self, content):
        if os.path.exists(self.cached_ausmap_qlr_file):
            os.remove(self.cached_ausmap_qlr_file)

        with codecs.open(self.cached_ausmap_qlr_file, "w", "utf-8") as f:
            f.write(content)
