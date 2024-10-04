from qgis.core import QgsLocatorFilter, QgsLocatorResult
from .utils.constants import PLUGIN_NAME

class LayerLocatorFilter(QgsLocatorFilter):
    def __init__(self, iface, layer_action_map):
        super().__init__()
        self.iface = iface
        self.layer_action_map = layer_action_map
    
    def name(self):
        return "ausmap_layer_locator_filter"

    def displayName(self):
        return f"{PLUGIN_NAME} Layers"
    
    def clone(self):
        return LayerLocatorFilter(self.iface, self.layer_action_map)

    def fetchResults(self, search_string, context, feedback):
        search_string = search_string.lower()
        for layer_name in self.layer_action_map.keys():
            if search_string in layer_name.lower():
                result = QgsLocatorResult()
                result.filter = self
                result.displayString = layer_name
                result.userData = layer_name
                self.resultFetched.emit(result)

    def triggerResult(self, result):
        layer_name = result.userData
        if layer_name in self.layer_action_map:
            # Get the QAction for the selected layer
            action = self.layer_action_map[layer_name]  
            action.trigger() 
     