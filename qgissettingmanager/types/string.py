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


# options:
# comboMode: can be data or text. It defines if setting is found directly in combobox text or rather in the userData.

from PyQt5.QtWidgets import QLineEdit, QButtonGroup, QComboBox
from qgis.core import QgsProject, QgsProject
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox

from ..setting import Setting
from ..setting_widget import SettingWidget


class String(Setting):
    def __init__(self, name, scope, default_value, options={}):
        Setting.__init__(self, name, scope, default_value, str, QgsProject.instance().readEntry, QgsProject.instance().writeEntry, options)

    def check(self, value):
        if type(value) != str:
            print(type(value))
            raise NameError('{}:: Invalid value for setting {}: {}. It must be a string.'.format(self.plugin_name, self.name, value))

    def config_widget(self, widget):
        if type(widget) == QLineEdit:
            return LineEditStringWidget(self, widget, self.options)
        elif type(widget) == QButtonGroup:
            return ButtonGroupStringWidget(self, widget, self.options)
        elif type(widget) == QComboBox:
            return ComboStringWidget(self, widget, self.options)
        elif type(widget) == QgsMapLayerComboBox:
            return MapLayerComboStringWidget(self, widget, self.options)
        elif type(widget) == QgsFieldComboBox:
            return FieldComboStringWidget(self, widget, self.options)
        else:
            raise NameError("SettingManager does not handle %s widgets for strings at the moment (setting: %s)" %
                (type(widget), self.name))


class LineEditStringWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.textChanged
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        self.widget.setText(value)

    def widget_value(self):
        return self.widget.text()


class ButtonGroupStringWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.buttonClicked
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        for button in self.widget.buttons():
            if value == button.objectName():
                button.setChecked(True)
                break

    def widget_value(self):
        value = ""
        for button in self.widget.buttons():
            if button.isChecked():
                value = button.objectName()
                break
        return value


class ComboStringWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        combo_mode = self.options.get("comboMode", "data")
        if combo_mode == 'data':
            self.widget.setCurrentIndex(self.widget.findData(value))
        elif combo_mode == 'text':
            self.widget.setCurrentIndex(self.widget.findText(value))
        else:
            raise NameError('invalid options for {}.comboMode: {}'.format(self.setting.name, combo_mode))

    def widget_value(self):
        combo_mode = self.options.get("comboMode", "data")
        if combo_mode == 'data':
            return self.widget.itemData(self.widget.currentIndex()) or ""
        elif combo_mode == 'text':
            return self.widget.currentText()
        else:
            raise NameError('invalid options for {}.comboMode: {}'.format(self.setting.name, combo_mode))


class MapLayerComboStringWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.layerChanged
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        self.widget.setLayer(QgsProject.instance().mapLayer(value))

    def widget_value(self):
        layer = self.widget.currentLayer()
        if layer is not None:
            return layer.id()
        else:
            return ""


class FieldComboStringWidget(SettingWidget):
    def __init__(self, setting, widget, options):
        signal = widget.currentIndexChanged
        SettingWidget.__init__(self, setting, widget, options, signal)

    def set_widget_value(self, value):
        self.widget.setField(value)

    def widget_value(self):
        return self.widget.currentField()








