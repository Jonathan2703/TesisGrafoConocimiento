import base64
from io import BytesIO
import matplotlib.pyplot as plt
from Orange.widgets.widget import OWWidget, Input
from Orange.data import Table
from Orange.widgets import gui

class VisualizadorImagenes(OWWidget):
    name = "Visualizador de Imágenes"
    description = "Visualizador de Imágenes"
    icon = "icons/image.svg"
    priority = 10

    class Inputs:
        image = Input("Imagen", Table)

    @Inputs.image
    def set_image(self, image):
        self.image = image

        # Clear the format combo and refill it
        self.format_combo.clear()
        self.names = []
        for row in self.image:
            self.names.append(str(row['name']))
        self.format_combo.addItems(self.names)

    def __init__(self):
        super().__init__()
        self.format=""
        self.format_combo = gui.comboBox(
            self.controlArea, self, "format", items=[], label="Format:"
        )
        self.format_combo.currentIndexChanged.connect(self.show_image)
        self.figure = None

    def show_image(self, index):
        row = self.image[index]
        image_str = row['image'].value
        image_bytes = base64.b64decode(image_str)
        image = plt.imread(BytesIO(image_bytes))
        if self.figure is None:
            self.figure = plt.figure()
        else:
            self.figure.clf()
        plt.imshow(image)
        plt.title(row['name'])
        plt.show()

