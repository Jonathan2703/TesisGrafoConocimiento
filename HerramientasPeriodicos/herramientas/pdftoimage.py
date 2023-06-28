from Orange.widgets.widget import OWWidget, Output, Input
from Orange.data import Table, Domain, StringVariable
from Orange.widgets import gui
import base64
import io
from pdf2image import convert_from_bytes

class PDFtoImagenWidget(OWWidget):
    name = "PDF to Image"
    description = "Convert PDF to Image"
    icon = "icons/pdf.svg"
    priority = 10

    class Outputs:
        image = Output("Image", Table)

    class Inputs:
        pdf = Input("Data", Table)

    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.format = "png"  # Add this line to initialize the format attribute
        self.format_combo = gui.comboBox(
            self.controlArea, self, "format", items=["png", "tiff"], label="Format:",
            callback=self.on_format_changed
        )
        self.create_button = gui.button(
            self.controlArea, self, "Create", callback=self.convert_to_image
        )

    @Inputs.pdf
    def set_pdf(self, pdf):
        self.pdf = pdf
    
    def on_format_changed(self):
        self.format = self.format_combo.currentText()

    def convert_to_image(self):
        if self.format == "png":
            # Code to convert PDF to PNG image format
            images = []
            for row in self.pdf:
                name = row["name"].value
                content_base64 = row["content"].value
                id_new= row["id"].value
                # Decode base64-encoded content to bytes
                content_bytes = base64.b64decode(content_base64)
                # Convert each page to PNG image
                images_list = convert_from_bytes(content_bytes)
                for i, img in enumerate(images_list):
                    # Convert PIL image to bytes
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format="PNG")
                    img_bytes = img_bytes.getvalue()

                    # Encode image bytes to base64-encoded string
                    image_base64 = base64.b64encode(img_bytes).decode("utf-8")

                    # Append the image as a new row to the output table
                    images.append({"name": f"{name} Page {i+1}", "image": image_base64, "id": id_new, "idpage": f"{id_new} Page {i+1}"})
            domain = Domain([], metas=[StringVariable("name"), StringVariable("image"), StringVariable("id"), StringVariable("idpage")])
            out_data = Table.from_list(domain, [[f["name"], f["image"], f["id"], f["idpage"]] for f in images])
            self.Outputs.image.send(out_data)
        elif self.format == "tiff":
            # Code to convert PDF to TIFF image format
            images = []
            for row in self.pdf:
                name = row["name"]
                content_base64 = row["content"].value
                id= row["id"].value
                # Decode base64-encoded content to bytes
                content_bytes = base64.b64decode(content_base64)
                # Convert each page to TIFF image
                images_list = convert_from_bytes(content_bytes)
                for i, img in enumerate(images_list):
                    # Convert PIL image to bytes
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format="TIFF")
                    img_bytes = img_bytes.getvalue()

                    # Encode image bytes to base64-encoded string
                    image_base64 = base64.b64encode(img_bytes).decode("utf-8")

                    # Append the image as a new row to the output table
                    images.append({"name": f"{name} Page {i+1}", "image": image_base64, "id": id, "idpage": f"{id} Page {i+1}"})
            domain = Domain([], metas=[StringVariable("name"), StringVariable("image"), StringVariable("id"), StringVariable("idpage")])
            out_data = Table.from_list(domain, [[f["name"], f["image"], f["id"], f["idpage"]] for f in images])
            self.Outputs.image.send(out_data)

        else:
            # Handle invalid format selection
            pass