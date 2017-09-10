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

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QLineEdit, QButtonGroup, QComboBox
from qgis.core import QgsProject, QgsMapLayerRegistry
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox

from ..setting import Setting


class String(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue, type=str)
        getProject = lambda: QgsProject.instance().readEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) != str and type(value) != unicode:
            print type(value)
            raise NameError("Setting %s must be a string." % self.name)

    def setWidget(self, widget):
        if type(widget) == QLineEdit:
            self.signal = "textChanged"
            self.widgetSetMethod = widget.setText
            self.widgetGetMethod = widget.text
        elif type(widget) == QButtonGroup:
            self.signal = "buttonClicked"
            self.widgetSetMethod = self.setButtonGroup
            self.widgetGetMethod = self.getButtonGroup
        elif type(widget) == QComboBox:
            self.signal = "activated"
            comboMode = self.options.get("comboMode", "data")
            if comboMode == 'data':
                self.widgetSetMethod = lambda(value): self.widget.setCurrentIndex(widget.findData(value))
                self.widgetGetMethod = lambda: widget.itemData(widget.currentIndex()) or ""
            elif comboMode == 'text':
                self.widgetSetMethod = lambda(value): self.widget.setCurrentIndex(widget.findText(value))
                self.widgetGetMethod = widget.currentText
        elif type(widget) in QgsMapLayerComboBox:
            self.signal = "layerChanged"
            self.widgetSetMethod = lambda(value): self.widget.setLayer(QgsMapLayerRegistry.instance().mapLayer(value))
            self.widgetGetMethod = lambda: widget.currentLayer().id()
        else:
            raise NameError("SettingManager does not handle %s widgets for strings at the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget

    def setButtonGroup(self, value):
        # for checkboxes
        if self.widget is None:
            return
        for button in self.widget.buttons():
            if value == button.objectName():
                button.setChecked(True)
                break

    def getButtonGroup(self):
        if self.widget is None:
            return
        value = ""
        for button in self.widget.buttons():
            if button.isChecked():
                value = button.objectName()
                break
        return value
