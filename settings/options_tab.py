import os

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from qgis.core import QgsSettings
from qgis.gui import (
    QgsFileWidget,
    QgsOptionsPageWidget,
    QgsOptionsWidgetFactory,
)

DESIGNER, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "settings.ui")
)


class AusMapOptionsFactory(QgsOptionsWidgetFactory):

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def icon(self):
        return QIcon(
            os.path.dirname(os.path.realpath(__file__))
            + os.sep
            + os.pardir
            + "/img/icon.png"
        )

    def createWidget(self, parent):
        return ConfigOptionsPage(parent, self.plugin)


class ConfigOptionsPage(QgsOptionsPageWidget, DESIGNER):

    def __init__(self, parent, plugin):
        super().__init__(parent)
        self.plugin = plugin
        self.setupUi(self)
        self.file_widget = self.findChild(QgsFileWidget, "custom_qlr_file")

        self.load_settings()

    def helpKey(self):
        return "settings"

    def load_settings(self):
        """Load the saved settings"""
        settings = QgsSettings()
        file_path = settings.value("custom_qlr_file", "", type=str)
        self.file_widget.setFilePath(file_path)

    def apply(self):
        """Save the current settings"""
        settings = QgsSettings()
        file_path = self.file_widget.filePath()
        settings.setValue("custom_qlr_file", file_path)

        self.plugin.reload_menu()
