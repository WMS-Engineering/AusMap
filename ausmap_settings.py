import os
from PyQt5 import QtWidgets, uic
from qgis.PyQt import QtCore

from .qgissettingmanager import *
from .utils import log_message

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'assets/am_settings.ui')
)


class KFSettings(SettingManager):
    settings_updated = QtCore.pyqtSignal()

    def __init__(self):
        SettingManager.__init__(self, 'AusMap')
        self.add_setting(String('username', Scope.Global, ''))
        self.add_setting(String('password', Scope.Global, ''))
        self.add_setting(Bool('use_custom_qlr_file', Scope.Project, False))
        self.add_setting(String('custom_qlr_file', Scope.Global, ''))
        self.add_setting(Bool('remember_settings', Scope.Global, False))


class KFSettingsDialog(WIDGET, BASE, SettingDialog):
    def __init__(self, settings):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        SettingDialog.__init__(self, settings)

        self.settings = settings
        if self.settings.value('remember_settings'):
            self.settings.set_value('use_custom_qlr_file', True)
            self.browseLocalFileButton.setEnabled(True)
        else:
            self.settings.set_value('use_custom_qlr_file', False)
            self.browseLocalFileButton.setEnabled(False)

        self.browseLocalFileButton.clicked.connect(self.browseLocalFile)
        self.use_custom_qlr_file.clicked.connect(self.useLocalChanged)

    def browseLocalFile(self):
        extension_list = ""
        extension_list += "Arc ASCII Grid (*.asc);;"
        extension_list += "ESRI Shapefile (*.shp);;"
        extension_list += "GeoTIFF (*.tif, *.tiff);;"
        extension_list += "JPEG JFIF (*.jpg, *.jpeg);;"
        extension_list += "KML - Keyhole Markup Language (*.kml);;"
        extension_list += "Mapinfo File (*.mif, *.tab);;"
        extension_list += "Portable Network Graphics (*.png);;"
        extension_list += "Qlr (*.qlr);;"
        file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Files",
            self.custom_qlr_file.text(),
            extension_list
        )
        if file:
            #self.settings.set_value('custom_qlr_file', file)
            self.custom_qlr_file.setText(str(file[0]))

    def useLocalChanged(self, checked):
        if self.use_custom_qlr_file.isChecked():
            self.browseLocalFileButton.setEnabled(True)
        else:
            self.browseLocalFileButton.setEnabled(False)

        self.settings.set_value('use_custom_qlr_file', checked)
        self.settings.set_value('remember_settings', checked)


    def emit_updated(self):
        self.settings_updated.emit()

