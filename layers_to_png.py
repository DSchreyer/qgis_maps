from qgis.core import QgsProject, QgsMapSettings, QgsMapRendererParallelJob
import os

dpi = 3.8

# Get the current QGIS project
project = QgsProject.instance()

layers = project.mapLayers().values()

# Create the output folder if it doesn't exist
project_folder = QgsProject.instance().homePath()
output_folder = os.path.join(project_folder, 'qgis_output')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the canvas
canvas = iface.mapCanvas()


# Loop through each layer and export as PNG
for layer in layers:
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
    print("Saved image for layer:", layer.name())