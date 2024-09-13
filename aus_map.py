# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AusMap
                                 A QGIS plugin
 AusMap is the essential plugin for Australian QGIS users, providing easy access to free Government Datasets and other web services.
                              -------------------
        begin                : 2017-09-10
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Water Modelling Solutions
        email                : admin@watermodelling.com.au
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
import codecs
import os.path
import datetime
from urllib.request import (
    urlopen,
    URLError,
    HTTPError
)
import webbrowser
from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog, QgsProject, QgsVectorLayer, QgsRasterLayer
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtCore import (
    QCoreApplication,
    QFileInfo,
    QUrl,
    QSettings,
    QTranslator,
    qVersion
)

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QPushButton
# Initialize Qt resources from file resources.py
from .ausmap_settings import(
    KFSettings,
    KFSettingsDialog
)

from .config import Config
from .layerlocatorfilter import LayerLocatorFilter
from .qgissettingmanager import *
from .utils.constants import ABOUT_FILE_URL, CONFIG_FILE_URL
from .utils import log_message


class AusMap:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.settings = KFSettings()
        self.settings.settings_updated.connect(self.reloadMenu)

        path = QFileInfo(os.path.realpath(__file__)).path()
        kf_path = path + '/kf/'
        if not os.path.exists(kf_path):
            os.makedirs(kf_path)

        self.settings.add_setting(String('cache_path', Scope.Global, kf_path))
        self.settings.add_setting(String('kf_qlr_url', Scope.Global, CONFIG_FILE_URL))
        self.layer_locator_filter = LayerLocatorFilter()
        self.iface.registerLocatorFilter(self.layer_locator_filter)
        self.local_about_file = kf_path + 'about.html'

        # An error menu object, set to None.
        self.error_menu = None

        # Categories
        self.categories = []
        self.nodes_by_index = {}
        self.node_count = 0

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
             path,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.networkManager = QNetworkAccessManager()

    def initGui(self):
        self.createMenu()

    def show_kf_error(self):
        message = u'Check connection and click menu AusMap->Settings->OK'
        self.iface.messageBar().pushMessage("No internet connection", message, level=QgsMessageBar.WARNING, duration=5)

    def show_kf_settings_warning(self):
            widget = self.iface.messageBar().createMessage(
                self.tr('AusMap'), self.tr(u'Username/Password not set or wrong. Click menu AusMap->Settings')
            )
            settings_btn = QPushButton(widget)
            settings_btn.setText(self.tr("Settings"))
            settings_btn.pressed.connect(self.settings_dialog)
            widget.layout().addWidget(settings_btn)
            self.iface.messageBar().pushWidget(widget, QgsMessageBar.WARNING, duration=10)

    def createMenu(self):
        self.config = Config(self.settings)
        self.config.kf_con_error.connect(self.show_kf_error)
        self.config.kf_settings_warning.connect(self.show_kf_settings_warning)
        self.config.load()
        self.categories = self.config.get_categories()
        self.category_lists = self.config.get_category_lists()
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_settings_path = os.path.join(os.path.dirname(__file__), 'assets/icon_settings.png')
        icon_about_path = os.path.join(os.path.dirname(__file__), 'assets/icon_about.png')

        self.menu = QMenu(self.iface.mainWindow().menuBar())
        self.menu.setObjectName(self.tr('AusMap'))
        self.menu.setTitle(self.tr('AusMap'))

        searchable_layers = []

        if self.error_menu:
            self.menu.addAction(self.error_menu)

        # Add menu object for each theme
        self.category_menus = []
        kf_helper = lambda _id: lambda: self.open_kf_node(_id)
        local_helper = lambda _id: lambda: self.open_local_node(_id)

        for category_list in self.category_lists:
            list_categorymenus = []
            for category in category_list:
                category_menu = QMenu()
                category_menu.setTitle(category['name'])
                for selectable in category['selectables']:
                    q_action = QAction(
                        selectable['name'], self.iface.mainWindow()
                    )
                    if selectable['source'] == 'kf':
                        q_action.triggered.connect(
                            kf_helper(selectable['id'])
                        )
                    else:
                        q_action.triggered.connect(
                            local_helper(selectable['id'])
                        )
                    category_menu.addAction(q_action)
                    searchable_layers.append(
                        {
                            'title': selectable['name'],
                            'category': category['name'],
                            'action': q_action
                        }
                    )
                list_categorymenus.append(category_menu)
                self.category_menus.append(category_menu)
            for category_menukuf in list_categorymenus:
                self.menu.addMenu(category_menukuf)
            self.menu.addSeparator()

        self.layer_locator_filter.set_searchable_layers(searchable_layers)
        is_custom_file = self.settings.value('remember_settings')
        if is_custom_file:
            custom_file = self.settings.value('custom_qlr_file')
            file_name, file_extension = os.path.splitext(custom_file)
            if '.qlr' not in file_extension:
                filename = os.path.basename(custom_file)
                file = os.path.splitext(filename)
                self.settings_menu = QAction(
                    self.tr(filename),
                    self.iface.mainWindow()
                )

                self.settings_menu.setObjectName(self.tr(filename))
                self.settings_menu.triggered.connect(self.custom_layer_dialog)
                self.menu.addAction(self.settings_menu)

        self.menu.addSeparator()
        # Settings menu
        self.settings_menu = QAction(
            QIcon(icon_settings_path),
            self.tr('Settings'),
            self.iface.mainWindow()
        )
        self.settings_menu.setObjectName(self.tr('Settings'))
        self.settings_menu.triggered.connect(self.settings_dialog)
        self.menu.addAction(self.settings_menu)

        # About Menu
        self.about_menu = QAction(
           QIcon(icon_about_path),
           self.tr('About the plugin'),
           self.iface.mainWindow()
        )
        self.about_menu.setObjectName(self.tr('About the plugin'))
        self.about_menu.triggered.connect(self.about_dialog)
        self.menu.addAction(self.about_menu)

        menu_bar = self.iface.mainWindow().menuBar()
        menu_bar.insertMenu(
            self.iface.firstRightStandardMenu().menuAction(), self.menu
        )

    def open_local_node(self, id):
        node = self.config.get_local_maplayer_node(id)
        self.open_node(node, id)

    def open_kf_node(self, id):
        node = self.config.get_kf_maplayer_node(id)
        layer = self.open_node(node, id)

    def open_node(self, node, id):
        QgsProject.instance().readLayer(node)
        layer = QgsProject.instance().mapLayer(id)
        if layer:
            layer = [layer for layer in QgsProject.instance().mapLayers().values()]
            return layer
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AusMap', message)

    def custom_layer_dialog(self):
        custom_file = self.settings.value('custom_qlr_file')

        file_name, file_extension = os.path.splitext(custom_file)
        if '.qlr' not in file_extension:
            file_name_split = file_name.split('/')
            final_file_name = file_name_split[len(file_name_split) - 1]
            vector_layer_extensions = [".kml", ".mid", ".mif", ".shp"]
            raster_layer_extensions = [".asc", ".jpg", ".png", ".tif"]
            if file_extension in vector_layer_extensions:
                vlayer = QgsVectorLayer(custom_file, final_file_name, "ogr")
                QgsProject.instance().addMapLayer(vlayer)
            elif file_extension in raster_layer_extensions:
                self.iface.addRasterLayer(custom_file, final_file_name)

    def settings_dialog(self):
        dlg = KFSettingsDialog(self.settings)
        dlg.set_widgets_from_values()
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            del dlg
            self.reloadMenu()

    def about_dialog(self):
        webbrowser.open(ABOUT_FILE_URL)

    def unload(self):
        # Remove settings if user not asked to keep them
        if self.settings.value('remember_settings') is False:
            self.settings.setValue('username', '')
            self.settings.setValue('password', '')
        self.clearMenu();

    def reloadMenu(self):
        self.clearMenu()
        self.createMenu()

    def clearMenu(self):
        # Remove the submenus
        for submenu in self.category_menus:
            if submenu:
                submenu.deleteLater()
        # remove the menu bar item
        if self.menu:
            self.menu.deleteLater()
