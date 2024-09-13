#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2016 Denis Rouzaud
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

from PyQt5.QtCore import pyqtSlot, QObject


class SettingWidget(QObject):
    def __init__(self, setting, widget, options, signal):
        QObject.__init__(self)

        self.setting = setting
        self.widget = widget
        self.options = options
        self.signal = signal
        self.connected = False

    def connect_widget_auto_update(self):
        """
        This connects the proper signal of the widget to self.set_value_from_widget
        """
        self.signal.connect(self.set_value_from_widget)
        self.connected = True

    def disconnect_widget_auto_update(self):
        """
        This disconnects the proper signal of the widget from self.set_value_from_widget
        """
        if self.connected:
            self.signal.disconnect(self.set_value_from_widget)
            self.connected = False

    def set_widget_value(self, value):
        """
        To be reimplemented in sub-class
        """
        pass

    def widget_value(self):
        """
        To be reimplemented in sub-class
        """
        return None

    def widget_test(self, value):
        """
        Method to test the UI, might be reimplemented in sub-class
        Returns True if the test can be run, False otherwise
        """
        # this will skip the disconnect/connect
        # so it should trigger the set_value_from_widget when in auto update mode
        self.set_widget_value(value)
        return True

    def set_widget_from_value(self):
        reconnect = False
        if self.connected:
            reconnect = True
            self.disconnect_widget_auto_update()
        self.set_widget_value(self.setting.value())
        if reconnect:
            self.connect_widget_auto_update()

    @pyqtSlot()
    def set_value_from_widget(self):
        self.setting.set_value(self.widget_value())