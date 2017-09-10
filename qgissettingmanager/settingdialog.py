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
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtGui import QDialog, QWidget, QButtonGroup

from settingmanager import Debug


class SettingDialog():
    def __init__(self, settingManager, setValuesOnDialogAccepted=True, setValueOnWidgetUpdate=False):
        if isinstance(self, QDialog) and setValuesOnDialogAccepted:
            self.accepted.connect(self.acceptDialog)

        self._settings = []
        for setting in settingManager.settings:
            for objectClass in (QWidget, QButtonGroup):
                widget = self.findChild(objectClass, setting.name)
                if widget is not None:
                    if Debug:
                        print "Widget found: %s" % setting.name
                    setting.setWidget(widget)
                    if setValueOnWidgetUpdate:
                        setting.setValueOnWidgetUpdateSignal()
                    self._settings.append(setting)
                    break

        # in case the widget has no showEvent
        self.setWidgetsFromValues()

    def showEvent(self, e):
        self.setWidgetsFromValues()

    def onBeforeAcceptDialog(self):
        """
        you can override this method in the PluginSettings subclass
        """
        return True

    def widgetList(self):
        wl = []
        for setting in self._settings:
            wl.append(setting.name)
        return wl

    def acceptDialog(self):
        if self.onBeforeAcceptDialog():
            self.setValuesFromWidgets()

    def setValuesFromWidgets(self):
        for setting in self._settings:
            if setting.widget is not None:
                setting.setValueFromWidget()

    def setWidgetsFromValues(self):
        for setting in self._settings:
            if setting.widget is not None:
                setting.setWidgetFromValue()
