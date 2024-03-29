from qgis.core import QgsProject, QgsMapSettings, QgsMapRendererParallelJob
from PyQt5.QtCore import QSize
import os

# Get the current QGIS project
project = QgsProject.instance()

# Get all layers
layers = project.mapLayers().values()

# Set the desired DPI (dots per inch)
desired_dpi = 300

# Create the output folder if it doesn't exist
output_folder = os.path.join(os.path.dirname(__file__), 'qgis_output')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the canvas
canvas = iface.mapCanvas()

# Loop through each layer and export as PNG
for layer in layers:
    settings = QgsMapSettings()
    settings.setLayers([layer])
    settings.setBackgroundColor(Qt.white)
    settings.setOutputSize(QSize(canvas.width(), canvas.height()))
    settings.setExtent(canvas.extent())
    settings.setDestinationCrs(project.crs())

    new_width = int(160 * desired_dpi)
    new_height = int(90 * desired_dpi)

    settings.setOutputSize(QSize(new_width, new_height))

    # Create a job with the map settings and output file path
    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()

    image = job.renderedImage()
    image.save(os.path.join(output_folder, f"{layer.name()}.png"), "png")
    print("Saved image for layer:", layer.name())