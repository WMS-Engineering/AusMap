# -*- coding: utf-8 -*-
from qgis.core import (QgsLocatorFilter,
                       QgsLocatorResult)


class LayerLocatorFilter( QgsLocatorFilter ):

    def __init__( self, data = None):
        super( LayerLocatorFilter, self ).__init__()
        if data is None:
            self.data = LayerLocatorFilterData()
        else:
            self.data = data
            
    def set_searchable_layers(self, searchable_layers):
        self.data.set_searchable_layers(searchable_layers)

    def clone(self):
        return LayerLocatorFilter( data = self.data )

    def name( self ):
        return 'AusMap'

    def displayName( self ):
        return self.tr( 'AusMap' )

    def priority( self ):
        return QgsLocatorFilter.Low

    def prefix( self ):
        return 'ausmap'

    def flags( self ):
        return QgsLocatorFilter.FlagFast

    def fetchResults( self, query, context, feedback ):
        matching_layers = self.data.get_matching_layers( query )
        for layer in matching_layers:
            result = QgsLocatorResult()
            result.filter = self
            result.displayString = layer['title']
            result.userData = layer['actionindex']
            result.score = 0
            
            self.resultFetched.emit(result)

    def triggerResult( self, result ):
        action = self.data.get_action( result.userData)
        action.activate(0)

class LayerLocatorFilterData():
    def __init__( self, parent=None ):
        self.searchable_layers = []

    def set_searchable_layers( self, searchable_layers ):
        self.searchable_layers = searchable_layers
        i=0
        self.actions = []
        for layer in self.searchable_layers:
            self.actions.append(layer['action'])
            layer['actionindex'] = i
            i = i+1
            layer['searchstring'] = self.create_search_string( layer )
            layer['title'] += ' (' + layer['category'] + ', AusMap)'

    def create_search_string( self, layer ):
        search_string = layer['category'] + ' ' + layer['title']
        search_string = search_string.replace( '/', ' ' )
        search_string = search_string.replace( '-', ' ' )
        search_string = search_string.replace( 'navn', ' ' )
        return ' ' + search_string.lower()

    def get_matching_layers( self, query ):
        search_terms = query.lower().split()
        term_count = len( search_terms )
        matching_layers = []
        for layer in self.searchable_layers:
            layer['points'] = 0
            for term in search_terms:
                if layer['searchstring'].find(' ' + term) > -1:
                    layer['points'] += 1
            if layer['points'] == term_count:
                matching_layers.append(layer)
        return matching_layers

    def get_action( self, index):
        return self.actions[index]