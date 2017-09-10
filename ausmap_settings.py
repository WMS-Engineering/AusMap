import os
from PyQt4 import QtGui, uic
from qgissettingmanager import SettingManager, SettingDialog

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'kf_settings.ui')
)


class KFSettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, 'AusMap')
        self.addSetting('username', 'string', 'global', '')
        self.addSetting('password', 'string', 'global', '')
        self.addSetting('use_custom_qlr_file', 'bool', 'global', False)
        self.addSetting('custom_qlr_file', 'string', 'global', '')
        self.addSetting('remember_settings', 'bool', 'global', False)
        
    def is_set(self):
        if self.value('username') and self.value('password'):
            return True
        return False

class KFSettingsDialog(QtGui.QDialog, FORM_CLASS, SettingDialog):
    def __init__(self, settings):
        QtGui.QDialog.__init__(self)
        #self.settings = settings
        self.setupUi(self)
        SettingDialog.__init__(self, settings)
        if self.use_custom_qlr_file.isChecked():
            self.browseLocalFileButton.setEnabled(True)
        else:
            self.browseLocalFileButton.setEnabled(False)

        self.browseLocalFileButton.clicked.connect(self.browseLocalFile)
        self.use_custom_qlr_file.clicked.connect(self.useLocalChanged)
        
    def browseLocalFile(self):
        file = QtGui.QFileDialog.getOpenFileName(
            self,
            "Lokal qlr",
            self.custom_qlr_file.text(),
            "Qlr (*.qlr)"
        )
        if file:
            #self.settings.set_value('custom_qlr_file', file)
            self.custom_qlr_file.setText(file)

    def useLocalChanged(self, checked):
        self.browseLocalFileButton.setEnabled(checked)

