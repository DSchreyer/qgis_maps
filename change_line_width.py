from qgis.core import QgsSymbolLayer
from PyQt5.QtCore import Qt

stream_width = 3
river_width = 3
middle_width = 1
top_width_large = 4
top_width_small = 3

# Check which layers are available based on the names
streams = None
top_small = None
top_large = None
bottom = None
middle = None

layers = iface.layerTreeView().selectedLayers()

for layer in layers:
    if layer.name() == "streams":
        streams = layer
    elif layer.name() == "Top Layer - Small":
        top_small = layer
    elif layer.name() == "Top Layer - Large":
        top_large = layer
    elif layer.name() == "Bottom Layer":
        bottom = layer
    elif layer.name() == "Middle-Layer-Streets":
        middle = layer
    elif layer.name() == "all_water":
        all_water = layer

# Modify the symbol widths for the available layers
if streams:
    streams.renderer().symbol().setWidth(stream_width)
    iface.layerTreeView().refreshLayerSymbology(streams.id())

if bottom:
    bottom.renderer().symbol().setWidth(river_width)
    iface.layerTreeView().refreshLayerSymbology(bottom.id())

if top_small:
    top_small.renderer().symbol().setWidth(top_width_small)
    iface.layerTreeView().refreshLayerSymbology(top_small.id())

if top_large:
    top_large.renderer().symbol().setWidth(top_width_large)
    iface.layerTreeView().refreshLayerSymbology(top_large.id())

if middle:
    middle.renderer().symbol().setWidth(middle_width)
    middle.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(middle.id())


# Example modification for one layer, repeat for others as needed
for layer in layers:
    renderer = layer.renderer()
    symbol = renderer.symbol()
    
    # Assuming the first symbol layer is a QgsSimpleLineSymbolLayer, adjust as necessary
    symbol_layer = symbol.symbolLayer(0)
    symbol_layer.setColor(QColor(0, 0, 0))  # Set the color to black
    if symbol_layer.layerType() == 'SimpleLine':
        symbol_layer.setPenJoinStyle(Qt.RoundJoin)
        symbol_layer.setPenCapStyle(Qt.RoundCap)

    layer.triggerRepaint()
