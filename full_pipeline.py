from qgis.core import QgsProject, QgsMapSettings, QgsMapRendererParallelJob
import os
from qgis.core import QgsSymbolLayer
from PyQt5.QtCore import Qt
import shutil
import subprocess
import glob
from svgutils.compose import Figure, SVG
from svgutils.transform import SVGFigure

# 1:72379 - 9 7 6 1 1 0 0 0 
# 1:50000 - 7.5 5.8 0.8 0.8 0 0
# 1:25000 - 5 4 0.6 0.6 0 0 

motorway_width = 11
primary_width = 8
secondary_width = 0
streets_width = 1
water_width = 0
stream_width = 0
river_width = 0
canal_width = 0
island_width = 0
coastline_width = 0

dpi = 3.5

# Check which layers are available based on the names
canal = None
river = None
secondary = None
primary = None
water = None
stream = None
motorway = None
streets = None
coastline = None



layers = iface.layerTreeView().selectedLayers()

def set_width(layer, width):
    layer.renderer().symbol().setWidth(width)
    iface.layerTreeView().refreshLayerSymbology(layer.id())

print("Starting layer width adjustments...")

for layer in layers:
    print(f"Processing layer: {layer.name()}")
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
    elif layer.name() == "ISLAND":
        island = layer
        island.renderer().symbol().symbolLayer(0).setStrokeWidth(water_width)
        island.renderer().symbol().symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
        iface.layerTreeView().refreshLayerSymbology(island.id())
    elif layer.name() == "STREAM":
        set_width(layer, stream_width)
    elif layer.name() == "COASTLINE":
        set_width(layer, coastline_width)
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

print("Layer width adjustments completed.")

# Get the current QGIS project
project = QgsProject.instance()

layers = project.mapLayers().values()

# Create the output folder if it doesn't exist
project_folder = QgsProject.instance().homePath()
output_folder = os.path.join(project_folder, 'qgis_output')

print("Creating output folder...")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
else: 
    shutil.rmtree(output_folder)
    os.makedirs(output_folder)

print(f"Output folder created at: {output_folder}")

# Get the canvas
canvas = iface.mapCanvas()

print("Starting PNG export...")

# Loop through each layer and export as PNG
for layer in layers:
    print(f"Exporting layer: {layer.name()}")
    settings = QgsMapSettings()
    settings.setLayers([layer])
    settings.setOutputSize(canvas.size())
    settings.setBackgroundColor(Qt.white)
    settings.setOutputSize(QSize(canvas.width()*dpi, canvas.height()*dpi))
    settings.setExtent(canvas.extent())
    settings.setDestinationCrs(project.crs())

    # Create a job with the map settings and output file path
    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()

    image = job.renderedImage()
    image.save(os.path.join(output_folder, f"{layer.name()}.png"), "png")

    print(f"Saved image for layer: {layer.name()}")

print("PNG export completed.")

# Define input folder path

# Define output folders within the input folder
bmp_output_folder = os.path.join(output_folder, 'bmp_output')
svg_output_folder = os.path.join(output_folder, 'svg_output')

# Remove existing files and directories
if os.path.exists(os.path.join(output_folder, 'OSM Standard.png')):
    os.remove(os.path.join(output_folder, 'OSM Standard.png'))

if os.path.exists(svg_output_folder):
    shutil.rmtree(svg_output_folder)

if os.path.exists(bmp_output_folder):
    shutil.rmtree(bmp_output_folder)

# Create output directories if they don't exist
os.makedirs(bmp_output_folder, exist_ok=True)
os.makedirs(svg_output_folder, exist_ok=True)

print("Starting PNG to BMP and SVG conversion...")

# Convert all PNG files in the input directory
for png_file in os.listdir(output_folder):
    if png_file.endswith('.png'):
        png_file_path = os.path.join(output_folder, png_file)
        filename = os.path.splitext(png_file)[0]

        # Define output file paths
        bmp_file_path = os.path.join(bmp_output_folder, f"{filename}.bmp")
        svg_file_path = os.path.join(svg_output_folder, f"{filename}.svg")

        # Convert PNG to BMP
        subprocess.run(['/opt/homebrew/bin/convert', png_file_path, bmp_file_path])

        # Trace BMP to SVG with Potrace
        subprocess.run(['/opt/homebrew/bin/potrace', '-b', 'svg', '-a', '0', '-t', '0', bmp_file_path, '-o', svg_file_path])

        print(f"Processed: {png_file_path}")

print("PNG to BMP and SVG conversion completed.")

# Generate svg stack
stack_folder = os.path.join(svg_output_folder, 'stack')
os.makedirs(stack_folder, exist_ok=True)
stack_svg_path = os.path.join(stack_folder, 'layer_stack.svg')

def merge_svgs(svg_folder, output_file):
    print(f"Merging SVG files from folder: {svg_folder}")
    # Get a list of all SVG files in the folder
    svg_files = glob.glob(f"{svg_folder}/*.svg")

    # Load all SVG files into SVG objects
    svgs = [SVG(svg_file) for svg_file in svg_files]

    # Create a new SVG figure with the size of the first SVG (assuming all SVGs have the same size)
    if svgs:
        first_svg = svgs[0]
        fig = SVGFigure(first_svg.width, first_svg.height)

        # Merge the SVG objects into the new figure
        for svg in svgs:
            fig.append(svg)

        # Save the merged SVG figure to the output file
        fig.save(output_file, encoding="utf-8")
        print(f"Merged SVG saved to: {output_file}")
    else:
        print("No SVG files found to merge.")

print("Starting SVG merge...")

merge_svgs(svg_output_folder, stack_svg_path)

print("Merged svg files.")