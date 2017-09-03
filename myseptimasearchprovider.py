# This is an example of how to make your plugin searchable through septima search
# Your plugin MUST have an attribute 'SeptimaSearchProvider' with this signature
# Example: self.SeptimaSearchProvider = MySeptimaSearchProvider()

from PyQt4 import (
    QtCore 
)
import json

class MySeptimaSearchProvider(QtCore.QObject):
    
    def __init__(self, kf_plugin, searchable_layers):
        # Mandatory because your search provider MUST extend QtCore.QObject
        QtCore.QObject.__init__(self)
        # Do other initialization here
        self.kf_plugin = kf_plugin
        self.searchable_layers = searchable_layers
        i=0
        self.actions = []
        for layer in self.searchable_layers:
            self.actions.append(layer['action'])
            layer['actionindex'] = i
            i = i+1
            self.make_searchable(layer)
            layer['title'] += ' (' + layer['category'] + ', ausmap)'
            
    def make_searchable(self, layer):
        search_string = layer['category'] + ' ' + layer['title']
        search_string = search_string.replace('/', ' ')
        search_string = search_string.replace('-', ' ')
        search_string = search_string.replace('navn', ' ')
        layer['searchstring'] = ' ' + search_string.lower()
        

    # Mandatory slot        
    @QtCore.pyqtSlot(str, int, result=str)
    def query(self, query, limit):
        search_results = []
        search_terms = query.lower().split()
        term_count = len(search_terms)
        hits = 0
        for layer in self.searchable_layers:
            layer['points'] = 0
            for term in search_terms:
                if layer['searchstring'].find(' ' + term) > -1:
                    layer['points'] += 1
            if layer['points'] == term_count:
                hits += 1
                if len(search_results) < limit:
                    search_results.append(
                        {
                            'title': layer['title'],
                            'actionindex': layer['actionindex']
                        }
                    )
        # Must return this structure
        result = {}
        result['status'] = 'ok'
        result['hits'] = hits
        result['results'] = search_results
        
        # Must return json
        return json.dumps(result)

    # Mandatory        
    def definition(self):
        # Return basic information about your self
        # iconURI is any valid URI, including a data URL:
        # eg.: {'singular': 'school', 'plural': 'school' [, 'iconURI': iconurl]} 
        return    {
            'singular': 'ausmap, lag',
            'plural': 'ausmap, lag',
            'iconURI': "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyLDE2TDE5LjM2LDEwLjI3TDIxLDlMMTIsMkwzLDlMNC42MywxMC4yN00xMiwxOC41NEw0LjYyLDEyLjgxTDMsMTQuMDdMMTIsMjEuMDdMMjEsMTQuMDdMMTkuMzcsMTIuOEwxMiwxOC41NFoiIC8+PC9zdmc+"
        }
    
    # Mandatory        
    def on_select(self, result):
        # The selected result is returned to you
        # Do your thing
        #self.kf_plugin.open_layer(result['filename'], result['layerid'])
        self.actions[result['actionindex']].activate(0)
