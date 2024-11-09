from qgis.core import QgsSymbolLayer
from PyQt5.QtCore import Qt

# 1:72379 - 9 7 6 1 1 0 0 0 
# 1:50000 - 7.5 5.8 0.8 0.8 0 0
# 1:25000 - 5 4 0.6 0.6 0 0 

motorway_width = 7.5
primary_width = 5.8
secondary_width = 1
streets_width = 1
water_width = 5
stream_width = 0
river_width = 0
canal_width = 0

dpi = 3.8

# Check which layers are available based on the names
canal = None
river = None
secondary = None
primary = None
water = None
stream = None
motorway = None
streets = None



layers = iface.layerTreeView().selectedLayers()

def set_width(layer, width):
    layer.renderer().symbol().setWidth(width)
    iface.layerTreeView().refreshLayerSymbology(layer.id())

for layer in layers:
    if layer.name() == "CANAL":
        set_width(layer, canal_width)
    elif layer.name() == "RIVER":
        set_width(layer, river_width)
    elif layer.name() == "SECONDARY":
        set_width(layer, secondary_width)
    elif layer.name() == "PRIMARY":
        set_width(layer, primary_width)
    elif layer.name() == "WATER":
        water = layer
        water.renderer().symbol().symbolLayer(0).setStrokeWidth(water_width)
        water.renderer().symbol().symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
        iface.layerTreeView().refreshLayerSymbology(water.id())
    elif layer.name() == "STREAM":
        set_width(layer, stream_width)
    elif layer.name() == "MOTORWAY":
        set_width(layer, motorway_width)
    elif layer.name() == "STREETS":
        set_width(layer, streets_width)
        
    renderer = layer.renderer()
    symbol = renderer.symbol()
    symbol_layer = symbol.symbolLayer(0)
    symbol_layer.setColor(QColor(0, 0, 0))  # Set the color to black
    if symbol_layer.layerType() == 'SimpleLine':
        symbol_layer.setPenJoinStyle(Qt.RoundJoin)
        symbol_layer.setPenCapStyle(Qt.RoundCap)

    layer.triggerRepaint()
