# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ausmap
                                 A QGIS plugin
 Easy access to WMS from ausmap (A service by The Danish geodataservice. Styrelsen for Dataforsyning og Effektivisering)
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
import codecs
import os.path
import datetime
from urllib2 import (
    urlopen,
    URLError,
    HTTPError
)
import webbrowser
from qgis.gui import QgsMessageBar
from qgis.core import *
from PyQt4.QtCore import (
    QCoreApplication,
    QFileInfo,
    QUrl,
    QSettings,
    QTranslator,
    qVersion
)

from PyQt4.QtGui import (
    QAction,
    QIcon,
    QMenu,
    QPushButton
)
from PyQt4 import QtXml
# Initialize Qt resources from file resources.py
from ausmap_settings import(
    KFSettings,
    KFSettingsDialog
)
# Import fails if QtWebKit is not correctly installed.
try:
    from ausmap_about import KFAboutDialog
except:
    from ausmap_about_alternative import KFAlternativeAboutDialog

import resources_rc
from qlr_file import QlrFile
from config import Config

from myseptimasearchprovider import MySeptimaSearchProvider
#Real URL"
#CONFIG_FILE_URL = 'http://apps2.ausmap.dk/qgis_knap_config/ausmap/qgis_plugin.qlr'

#Develop
#CONFIG_FILE_URL = 'http://labs.septima.dk/qgis-kf-knap/kortforsyning_data.qlr'
#CONFIG_FILE_URL = 'http://labs.septima.dk/qgis-kf-knap/kortforsyning_data_SDFE.qlr'
##test version: 'http://labs.septima.dk/qgis-kf-knap/kortforsyning_data_inkl_restricteddata.qlr'
CONFIG_FILE_URL = 'http://apps2.ausmap.dk/qgis_knap_config/ausmap/kf/kortforsyning_data.qlr'

ABOUT_FILE_URL = 'http://apps2.ausmap.dk/qgis_knap_config/ausmap/kf/about.html'
FILE_MAX_AGE = datetime.timedelta(hours=12)

def log_message(message):
    QgsMessageLog.logMessage(message, 'ausmap plugin')

class ausmap:
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
        
        path = QFileInfo(os.path.realpath(__file__)).path()
        kf_path = path + '/kf/'
        if not os.path.exists(kf_path):
            os.makedirs(kf_path)
            
        self.settings.addSetting('cache_path', 'string', 'global', kf_path)
        self.settings.addSetting('kf_qlr_url', 'string', 'global', CONFIG_FILE_URL)

        self.local_about_file = kf_path + 'about.html'

        # An error menu object, set to None.
        self.error_menu = None

        # Categories
        self.categories = []
        self.nodes_by_index = {}
        self.node_count = 0

        # Read the about page
        self.read_about_page()

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

    def read_about_page(self):
        load_remote_about = True

        local_file_exists = os.path.exists(self.local_about_file)
        if local_file_exists:
            local_file_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(self.local_about_file)
            )
            load_remote_about = local_file_time < datetime.datetime.now() - FILE_MAX_AGE

        if load_remote_about:
            try:
                response = urlopen(ABOUT_FILE_URL)
                about = response.read()
            except Exception, e:
                log_message('No contact to the configuration at ' + ABOUT_FILE_URL + '. Exception: ' + str(e))
                if not local_file_exists:
                    self.error_menu = QAction(
                        self.tr('No contact to Kortforsyning'),
                        self.iface.mainWindow()
                    )
                return
            self.write_about_file(about)

    def write_about_file(self, content):
        if os.path.exists(self.local_about_file):
            os.remove(self.local_about_file)

        with codecs.open(self.local_about_file, 'w') as f:
            f.write(content)
            
    def initGui(self):
        self.createMenu()
        
    def show_kf_error(self):
        message = u'Check connection and click menu ausmap->Settings->OK'
        self.iface.messageBar().pushMessage("No contact to ausmap", message, level=QgsMessageBar.WARNING, duration=5)

    def show_kf_settings_warning(self):
            widget = self.iface.messageBar().createMessage(
                self.tr('ausmap'), self.tr(u'Username/Password not set or wrong. Click menu ausmap->Settings')
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

        #icon_path = ':/plugins/ausmap/icon.png'
        icon_path = ':/plugins/ausmap/settings-cog.png'
        icon_path_info = ':/plugins/ausmap/icon_about.png'

        self.menu = QMenu(self.iface.mainWindow().menuBar())
        self.menu.setObjectName(self.tr('ausmap'))
        self.menu.setTitle(self.tr('ausmap'))
        
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
        self.septimasearchprovider = MySeptimaSearchProvider(self, searchable_layers)

        # Add settings
        self.settings_menu = QAction(
            QIcon(icon_path),
            self.tr('Settings'),
            self.iface.mainWindow()
        )
        self.settings_menu.setObjectName(self.tr('Settings'))
        self.settings_menu.triggered.connect(self.settings_dialog)
        self.menu.addAction(self.settings_menu)

        # Add about
        self.about_menu = QAction(
            QIcon(icon_path_info),
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
        QgsProject.instance().read(node)
        layer = QgsMapLayerRegistry.instance().mapLayer(id)
        if layer:
            self.iface.legendInterface().refreshLayerSymbology(layer)
            #self.iface.legendInterface().moveLayer(layer, 0)
            self.iface.legendInterface().refreshLayerSymbology(layer)
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
        return QCoreApplication.translate('ausmap', message)

    # Taken directly from menu_from_project
    def getFirstChildByTagNameValue(self, elt, tagName, key, value):
        nodes = elt.elementsByTagName(tagName)
        i = 0
        while i < nodes.count():
            node = nodes.at(i)
            idNode = node.namedItem(key)
            if idNode is not None:
                child = idNode.firstChild().toText().data()
                # layer found
                if child == value:
                    return node
            i += 1
        return None

    def settings_dialog(self):
        dlg = KFSettingsDialog(self.settings)
        dlg.setWidgetsFromValues()
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            del dlg
            self.reloadMenu()

    def about_dialog(self):
        if 'KFAboutDialog' in globals():
            dlg = KFAboutDialog()
            dlg.webView.setUrl(QUrl(self.local_about_file))
            dlg.webView.urlChanged
            dlg.show()
            result = dlg.exec_()

            if result == 1:
                del dlg
        else:
            dlg = KFAlternativeAboutDialog()
            dlg.buttonBox.accepted.connect(dlg.accept)
            dlg.buttonBox.rejected.connect(dlg.reject)
            dlg.textBrowser.setHtml(self.tr('<p>QGIS is having trouble showing the content of this dialog. Would you like to open it in an external browser window?</p>'))
            dlg.show()
            result = dlg.exec_()

            if result:
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