from qgis.core import QgsProject, QgsMapSettings, QgsMapRendererParallelJob
import os
from qgis.core import QgsSymbolLayer
from PyQt5.QtCore import Qt, QSize
import shutil
import subprocess
import glob
from svgutils.compose import Figure, SVG
from svgutils.transform import SVGFigure
from combine_svg_paths import process_folder as combine_svg_paths
from merge_svgs import merge_svgs

# 
# Keep sizes constant - Width Factor around 0.66 -> 12 - 11 - 8 
# Largest upper street starts at 12 - Small size difference between motorway and primary street when secondary is shown
# Smalles upper street starts at 8

motorway_width = 10
primary_width = 8.4
secondary_width = 6.6
streets_width = 1
water_width = 3
stream_width = 0
river_width = 3
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

        try:
            # Convert PNG to BMP
            print(f"Converting {png_file_path} to {bmp_file_path}")
            subprocess.run(['/opt/homebrew/bin/convert', png_file_path, bmp_file_path], check=True)

            # Trace BMP to SVG with Potrace
            print(f"Tracing {bmp_file_path} to {svg_file_path}")
            subprocess.run(['/opt/homebrew/bin/potrace', '-b', 'svg', '-a', '0', '-t', '0', bmp_file_path, '-o', svg_file_path], check=True)

            print(f"Processed: {png_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {png_file_path}: {e}")

print("PNG to BMP and SVG conversion completed.")

print("Combine SVG paths...")

combine_folder = os.path.join(output_folder, 'combined')

try:
    # Directly call the process_folder function from combine_svg_paths.py
    combine_svg_paths(svg_output_folder, combine_folder)
except Exception as e:
    print(f"Error combining SVG paths: {e}")

print("Starting SVG merge...")

# Generate svg stack
stack_folder = os.path.join(output_folder, 'stack')
os.makedirs(stack_folder, exist_ok=True)
stack_svg_path = os.path.join(stack_folder, 'layer_stack.svg')

try:
    merge_svgs(combine_folder, stack_svg_path)
    print("Merged svg files.")
except Exception as e:
    print(f"Error merging SVG files: {e}")

print("Finished processing SVG files.")