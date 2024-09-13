#-----------------------------------------------------------
#
# QGIS Setting Manager
# Copyright (C) 2016 Denis Rouzaud
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QDialog, QDoubleSpinBox, QComboBox, QListWidget
from qgis.gui import QgsCollapsibleGroupBox
from ..setting_dialog import SettingDialog, UpdateMode
from .my_settings import MySettings


class MySettingsDialog(QDialog, SettingDialog):
    def __init__(self, setting_name, widget_class, mode=UpdateMode.DialogAccept):
        QDialog.__init__(self)

        self.settings = MySettings()
        w = widget_class(self)
        w.setObjectName(setting_name)

        # setup UI
        if setting_name.startswith('bool_') and widget_class == QgsCollapsibleGroupBox:
            w.setCheckable(True)
        if setting_name.startswith('double_') and widget_class == QDoubleSpinBox:
            w.setDecimals(5)
        if setting_name.startswith('integer_') and widget_class == QComboBox:
            for x in (1, 2, 3):
                w.addItem(str(x))
        if setting_name.startswith('string_') and widget_class == QComboBox:
            w.addItem('default_string')
            w.addItem('new_string')
        if setting_name.startswith('stringlist_') and widget_class == QListWidget:
            w.addItems(('abc', 'def', 'ghi', 'random', 'qwe', 'rtz', 'uio'))

        # init SettingDialog
        SettingDialog.__init__(self, self.settings, mode)
