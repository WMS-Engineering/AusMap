#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
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
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QCheckBox
from qgis.core import QgsProject
from ..setting import Setting
from ..setting_widget import SettingWidget
from ..setting_manager import Debug


class Bool(Setting):

    def __init__(self, name, scope, default_value, options={}):
        Setting.__init__(self, name, scope, default_value, bool, QgsProject.instance().readBoolEntry, QgsProject.instance().writeEntryBool, options)

    def check(self, value):
        if type(value) != bool:
            raise NameError("Setting %s must be a boolean." % self.name)
        
    def config_widget(self, widget):
        if type(widget) == QCheckBox:
            return CheckBoxBoolWidget(self, widget, self.options)
        elif hasattr(widget, "isCheckable") and widget.isCheckable():
            return CheckableBoolWidget(self, widget, self.options)
        else:
            print(type(widget))
            raise NameError("SettingManager does not handle %s widgets for booleans at the moment (setting: %s)" %
                            (type(widget), self.name))


class CheckBoxBoolWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.stateChanged
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        if Debug:
            print("Bool: set_widget_value: {0}{1}".format(value, self.setting.name))
        self.widget.setChecked(value)

    def widget_value(self):
        return self.widget.isChecked()


class CheckableBoolWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.clicked
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        self.widget.setChecked(value)

    def widget_value(self):
        return self.widget.isChecked()

    def widget_test(self, value):
        print('cannot test checkable groupbox at the moment')
        return False