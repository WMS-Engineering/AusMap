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

import qgis
from qgis.testing import start_app, unittest

import nose2

from ..setting_dialog import UpdateMode
from .my_settings import MySettings
from .my_settings_dialog import MySettingsDialog



# TODO: remaining tests:
# string with QgsMapLayerComboBox and QButtonGroup and also comboMode:data
# stringlist with QGroupBox


def params(settings):
    params = []
    for s_name, setting_ in settings.items():
        for widget_class in setting_['widgets']:
            params.append(('{}_{}'.format(s_name, widget_class.__name__), s_name, widget_class))
    return params


class TestDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_app()

    def test_dialog_accept_update(self):
        for param in params(MySettings().settings_cfg):
            yield self.check_dialog_accept_update, param[0], param[1], param[2]

    def check_dialog_accept_update(self, test_name, name, widget_class):
        # get setting config
        setting_cfg = MySettings().settings_cfg[name]

        # this will reset to default with new call of MySettings within MySettingsDialog
        MySettings().remove(name)

        # create dialog
        self.dlg = MySettingsDialog(name, widget_class, UpdateMode.DialogAccept)
        self.dlg.show()

        # control that the widget is detected
        self.assertIn(name, self.dlg.widget_list())

        # get widget
        setting_widget = self.dlg.setting_widget(name)
        self.assertIsNotNone(setting_widget)

        # controls that widget is set to default
        self.assertEqual(setting_widget.widget_value(), setting_cfg['default'])

        # set value
        setting_widget.set_widget_value(setting_cfg['new_value'])

        # controls that widget has been update
        self.assertEqual(setting_widget.widget_value(), setting_cfg['new_value'])

        # accept dialog
        self.dlg.accept()

        # check setting has now new value
        self.assertEqual(MySettings().value(name), setting_cfg['new_value'])
        self.dlg.close()

        # reset setting
        MySettings().remove(name)

    def test_dialog_auto_update(self):
        for param in params(MySettings().settings_cfg):
            yield self.check_dialog_auto_update, param[0], param[1], param[2]

    def check_dialog_auto_update(self, test_name, name, widget_class):
        # get setting config
        setting_cfg = MySettings().settings_cfg[name]

        # this will reset to default with new call of MySettings within MySettingsDialog
        MySettings().remove(name)

        # test with direct update
        self.dlg = MySettingsDialog(name, widget_class, UpdateMode.WidgetUpdate)
        self.dlg.show()

        # get widget
        setting_widget = self.dlg.setting_widget(name)

        # controls that widget is set to default
        self.assertEqual(setting_widget.widget_value(), setting_cfg['default'])

        # set value
        if setting_widget.widget_test(setting_cfg['new_value']) is not False:
            self.assertEqual(MySettings().value(name), setting_cfg['new_value'])
        else:
            # cannot test UI
            print('{} cannot be run for set_value_on_widget_update = True'.format(test_name))
        self.dlg.close()

        # reset setting
        MySettings().remove(name)


if __name__ == '__main__':
    nose2.main()
