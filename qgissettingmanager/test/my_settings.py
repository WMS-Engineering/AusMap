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

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QDoubleSpinBox, QLineEdit, QSpinBox, QSlider, QComboBox, QListWidget
from qgis.gui import QgsCollapsibleGroupBox, QgsColorButton

from .. import *

pluginName = "test_plugin"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        settings_root = {'bool': {'class': Bool, 'default': True, 'options': {}, 'new_value': False, 'widgets': (QCheckBox, QgsCollapsibleGroupBox)},
                         'color': {'class': Color, 'default': QColor(100, 100, 100, 100), 'options': {'allowAlpha': True}, 'new_value': QColor(30, 30, 30, 30), 'widgets': (QgsColorButton, QLabel, QPushButton)},
                         'double': {'class': Double, 'default': 0.12345, 'options': {}, 'new_value': 1.98765, 'widgets': (QDoubleSpinBox, QLineEdit)},
                         'integer': {'class': Integer, 'default': 1, 'options': {}, 'new_value': 2, 'widgets': (QLineEdit, QSpinBox, QSlider, QComboBox)},
                         'string': {'class': String, 'default': 'default_string', 'options': {'comboMode': 'text'}, 'new_value': 'new_string', 'widgets': (QLineEdit, QComboBox)},
                         'stringlist': {'class': Stringlist, 'default': ['abc', 'def', 'ghi'], 'options': {}, 'new_value': ['qwe', 'rtz', 'uio'], 'widgets': [QListWidget]}}


        self.settings_cfg = {}
        scopes = {'project': Scope.Project, 'global': Scope.Global}
        for s_name, setting_ in settings_root.items():
            for scope_str, scope_val in scopes.items():
                # TODO python 3 use enum
                setting_name = '{}_{}'.format(s_name, scope_str)
                self.settings_cfg[setting_name] = setting_
                self.add_setting(setting_['class'](setting_name, scope_val, setting_['default'], setting_['options']))



