import codecs
import os.path
from datetime import datetime, timezone
from urllib.request import urlopen

from PyQt5.QtCore import QFile, QIODevice, QObject
from qgis.core import Qgis, QgsMessageLog

from .qlr_file import QlrFile


class AusMapConfig(QObject):

    def __init__(self, settings):
        super(AusMapConfig, self).__init__()
        self.settings = settings
        self.cached_ausmap_qlr_file = os.path.join(
            self.settings.value("cache_path"), "ausmap_data.qlr"
        )
        self.qlr_file = None
        self.categories = []

    def load(self):
        self.qlr_file = self._get_qlr_file()
        self.categories = self._parse_categories() if self.qlr_file else []

    def get_categories(self):
        return self.categories

    def get_maplayer_node(self, layer_id):
        return self.qlr_file.get_maplayer_node(layer_id)

    def _parse_categories(self):
        """Parse categories and layers from the QLR file."""
        return [
            {
                "name": group["name"],
                "selectables": [
                    {
                        "type": "layer",
                        "source": "ausmap",
                        "name": layer["name"],
                        "id": layer["id"],
                    }
                    for layer in group["layers"]
                ],
            }
            for group in self.qlr_file.get_groups_with_layers()
            if group["layers"]
        ]

    def _get_qlr_file(self):

        # Check the last modified date of the remote QLR file
        with open(
            os.path.join(os.path.dirname(__file__), "qlr_last_modified.txt"),
            "r",
        ) as last_modified_file:
            last_modified_timestamp = last_modified_file.readline().rstrip()
            last_modified_remote_qlr = datetime.strptime(
                last_modified_timestamp, "%Y-%m-%d %H:%M:%S%z"
            )

        # Check if the local QLR file is up to date
        if os.path.exists(self.cached_ausmap_qlr_file):
            local_file_time = datetime.fromtimestamp(
                os.path.getmtime(self.cached_ausmap_qlr_file), tz=timezone.utc
            )
            if local_file_time > last_modified_remote_qlr:
                return self._read_cached_qlr()

        # Fetch remote QLR and save it locally
        try:
            remote_qlr_content = self._get_remote_qlr()
            self._write_local_qlr(remote_qlr_content)
            return QlrFile(remote_qlr_content)

        except Exception as error:
            QgsMessageLog.logMessage(
                (
                    "An unexpected error occurred while"
                    f"fetching QLR file: {str(error)}"
                ),
                level=Qgis.Critical,
            )

    def _read_cached_qlr(self):
        f = QFile(self.cached_ausmap_qlr_file)
        f.open(QIODevice.ReadOnly)
        content = f.readAll()
        return QlrFile(content)

    def _get_remote_qlr(self):
        with urlopen(self.settings.value("ausmap_qlr")) as response:
            return response.read().decode("utf-8")

    def _write_local_qlr(self, content):
        if os.path.exists(self.cached_ausmap_qlr_file):
            os.remove(self.cached_ausmap_qlr_file)
        with codecs.open(self.cached_ausmap_qlr_file, "w", "utf-8") as f:
            f.write(content)
