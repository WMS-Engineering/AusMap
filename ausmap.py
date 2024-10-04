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
from qgis.core import QgsMessageLog, QgsProject, QgsVectorLayer, QgsRasterLayer, QgsSettings
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


from .config import Config
from .layer_locator_filter import LayerLocatorFilter
from .utils.constants import ABOUT_FILE_URL, CONFIG_FILE_URL, PLUGIN_NAME
from .utils import log_message

from .settings import AusMapOptionsFactory


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

        self.settings = QgsSettings()
        # self.settings.settings_updated.connect(self.reloadMenu)

        path = QFileInfo(os.path.realpath(__file__)).path()
        cache_path = path + '/data/'
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self.settings.setValue('cache_path', cache_path)
        self.settings.setValue('ausmap_qlr', CONFIG_FILE_URL)

        self.error_menu = None

        # Initialize locale - this is maybe not needed 
        locale = QSettings().value('locale/userLocale') # en_AU
        locale_path = os.path.join(
             path,
            'i18n',
            '{}.qm'.format(locale))
        
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


    def initGui(self):
        self.options_factory = AusMapOptionsFactory(self)
        self.options_factory.setTitle(PLUGIN_NAME)
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        self.create_menu()

    def show_kf_error(self):
        message = u'Check connection and click menu AusMap->Settings->OK'
        self.iface.messageBar().pushMessage("No internet connection", message, level=QgsMessageBar.WARNING, duration=5)

    def show_kf_settings_warning(self):
        widget = self.iface.messageBar().createMessage(
            PLUGIN_NAME, self.tr(u'Username/Password not set or wrong. Click menu AusMap->Settings')
        )
        settings_btn = QPushButton(widget)
        settings_btn.setText(self.tr("Settings"))
        settings_btn.pressed.connect(self.settings_dialog)
        widget.layout().addWidget(settings_btn)
        self.iface.messageBar().pushWidget(widget, QgsMessageBar.WARNING, duration=10)

    def create_menu(self):
        self.config = Config(self.settings)
        self.config.kf_con_error.connect(self.show_kf_error)
        self.config.kf_settings_warning.connect(self.show_kf_settings_warning)
        self.config.load()

        self.categories = self.config.get_categories()
        self.category_lists = self.config.get_category_lists()
        
        self.menu = QMenu(self.iface.mainWindow().menuBar())
        self.menu.setObjectName(PLUGIN_NAME)
        self.menu.setTitle(PLUGIN_NAME)

        if self.error_menu:
            self.menu.addAction(self.error_menu)

        # Add menu object for each category
        self.category_menus = []
        helper = lambda _id: lambda: self.open_ausmap_node(_id)
        local_helper = lambda _id: lambda: self.open_local_node(_id)
        layer_action_map = {} # Used for the locator filter

        for category_list in self.category_lists:
            list_categorymenus = []
            for category in category_list:
                category_menu = QMenu()
                category_menu.setTitle(category['name'])
                for selectable in category['selectables']:
                    action = QAction(
                        selectable['name'], self.iface.mainWindow()
                    )
                    if selectable['source'] == 'ausmap':
                        action.triggered.connect(
                            helper(selectable['id'])
                        )
                    else:
                        action.triggered.connect(
                            local_helper(selectable['id'])
                        )
                    category_menu.addAction(action)

                    layer_action_map[selectable['name']] = action
                  
                list_categorymenus.append(category_menu)
                self.category_menus.append(category_menu)
            for category_menukuf in list_categorymenus:
                self.menu.addMenu(category_menukuf)
            self.menu.addSeparator()

        
        self.layer_locator_filter = LayerLocatorFilter(self.iface, layer_action_map)
        self.iface.registerLocatorFilter(self.layer_locator_filter)

        # About menu item
        icon_about_path = os.path.join(os.path.dirname(__file__), 'assets/icon_about.png')
        self.about_menu = QAction(
           QIcon(icon_about_path),
           self.tr('About the plugin'),
           self.iface.mainWindow()
        )
        self.about_menu.triggered.connect(self.about_plugin)
        self.menu.addAction(self.about_menu)

        menu_bar = self.iface.mainWindow().menuBar()
        menu_bar.insertMenu(
            self.iface.firstRightStandardMenu().menuAction(), self.menu
        )

    def open_local_node(self, id):
        node = self.config.get_local_maplayer_node(id)
        self.open_node(node, id)

    def open_ausmap_node(self, id):
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
        return QCoreApplication.translate(PLUGIN_NAME, message)

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

    def about_plugin(self):
        webbrowser.open(ABOUT_FILE_URL)

    def unload(self):
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)
        self.iface.deregisterLocatorFilter(self.layer_locator_filter)
        self.clearMenu()

    def reload_menu(self):
        self.clearMenu()
        self.create_menu()

    def clearMenu(self):
        # Remove the sub-menus and the menu bar item
        for submenu in self.category_menus:
            if submenu:
                submenu.deleteLater()
        if self.menu:
            self.menu.deleteLater()
