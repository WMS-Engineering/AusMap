import os.path
import webbrowser

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu
from qgis.core import QgsProject, QgsSettings

from .config import Config
from .constants import ABOUT_FILE_URL, PLUGIN_NAME, QLR_URL
from .layer_locator_filter import LayerLocatorFilter
from .settings import AusMapOptionsFactory


class AusMap:
    """QGIS Plugin Implementation"""

    def __init__(self, iface):
        """Constructor
        :param iface: An interface instance that will be passed to this class
                      which provides the hook by which you can manipulate the
                      QGIS application at run time.
        :type iface:  QgsInterface
        """
        self.iface = iface  # Reference to the QGIS interface
        self.settings = QgsSettings()

        path = QFileInfo(os.path.realpath(__file__)).path()
        cache_path = path + "/data/"
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self.settings.setValue("cache_path", cache_path)
        self.settings.setValue("ausmap_qlr", QLR_URL)

    def initGui(self):
        self.options_factory = AusMapOptionsFactory(self)
        self.options_factory.setTitle(PLUGIN_NAME)
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        self.create_menu()

    def create_menu(self):
        self.config = Config(self.settings)
        self.config.load()
        self.groups_and_layers = self.config.get_groups_and_layers()

        self.menu = QMenu(self.iface.mainWindow().menuBar())
        self.menu.setObjectName(PLUGIN_NAME)
        self.menu.setTitle(PLUGIN_NAME)

        helper = lambda _id: lambda: self.open_ausmap_node(_id)
        local_helper = lambda _id: lambda: self.open_local_node(_id)

        self.menu_with_actions = []
        layer_action_map = {}  # Used for the locator filter

        for category in self.groups_and_layers:
            for group in category:
                group_menu = QMenu()
                group_menu.setTitle(group["name"])
                for layer in group["selectables"]:
                    action = QAction(layer["name"], self.iface.mainWindow())
                    if layer["source"] == "ausmap":
                        action.triggered.connect(helper(layer["id"]))
                    else:
                        action.triggered.connect(local_helper(layer["id"]))
                    group_menu.addAction(action)

                    layer_action_map[layer["name"]] = action

                self.menu.addMenu(group_menu)
                self.menu_with_actions.append(group_menu)

            self.menu.addSeparator()

        # Add locator filter
        self.layer_locator_filter = LayerLocatorFilter(
            self.iface, layer_action_map
        )
        self.iface.registerLocatorFilter(self.layer_locator_filter)

        # Add About the plugin menu item
        icon_about_path = os.path.join(
            os.path.dirname(__file__), "img/icon_about.png"
        )
        self.about_menu = QAction(
            QIcon(icon_about_path),
            "About the plugin",
            self.iface.mainWindow(),
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
        node = self.config.get_ausmap_maplayer_node(id)
        self.open_node(node, id)

    def open_node(self, node, id):
        QgsProject.instance().readLayer(node)
        layer = QgsProject.instance().mapLayer(id)
        if layer:
            layer = [
                layer for layer in QgsProject.instance().mapLayers().values()
            ]
            return layer
        else:
            return None

    def about_plugin(self):
        webbrowser.open(ABOUT_FILE_URL)

    def unload(self):
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)
        self.iface.deregisterLocatorFilter(self.layer_locator_filter)
        self.options_factory = None
        self.layer_locator_filter = None
        self.clear_menu()

    def reload_menu(self):
        self.clear_menu()
        self.iface.deregisterLocatorFilter(self.layer_locator_filter)
        self.layer_locator_filter = None
        self.create_menu()

    def clear_menu(self):
        # Remove the sub-menus and the menu bar item
        for submenu in self.menu_with_actions:
            if submenu:
                submenu.deleteLater()
        if self.menu:
            self.menu.deleteLater()
        self.menu = None
