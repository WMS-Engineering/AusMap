# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ausmapSettingsDialog
                                 A QGIS plugin
 Easy access to WMS from ausmap
                             -------------------
        begin                : 2015-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2015 Agency for Data supply and Efficiency
        email                : ausmap@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt4 import QtGui, uic
from qgissettingmanager import SettingManager, SettingDialog

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'kf_settings.ui')
)


class KFSettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, 'ausmap')
        self.addSetting('username', 'string', 'global', '')
        self.addSetting('password', 'string', 'global', '')
        self.addSetting('use_custom_qlr_file', 'bool', 'global', False)
        self.addSetting('custom_qlr_file', 'string', 'global', '')
        self.addSetting('kf_only_background', 'bool', 'global', False)
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
            self.kf_only_background.setEnabled(True)
            self.browseLocalFileButton.setEnabled(True)
        else:
            self.kf_only_background.setEnabled(False)
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
        self.kf_only_background.setEnabled(checked)
        self.browseLocalFileButton.setEnabled(checked)

