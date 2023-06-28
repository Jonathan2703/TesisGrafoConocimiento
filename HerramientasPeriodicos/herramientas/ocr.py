from Orange.widgets.widget import OWWidget, Output, Input
from Orange.data import Table, Domain, StringVariable
import base64
import numpy as np
import cv2
import pytesseract

class OcrWidget(OWWidget):
    name = "Ocr"
    description = "Ocr with tesseract"
    icon = "icons/ocr.svg"
    priority = 10

    class Inputs:
        images = Input("Images", Table)
    
    class Outputs:
        text = Output("Text", Table)
    
    def __init__(self):
        super().__init__()
        
    
    @Inputs.images
    def set_images(self, images):
        self.images = images
        self.ocr_images()
    
    def ocr_images(self):
        ocr=[]
        for row in self.images:
            name = row["name"]
            image_base64 = row["image"].value
            id = row["id"]
            idpage= row["idpage"]
            image_bytes = base64.b64decode(image_base64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
            text = pytesseract.image_to_string(image)
            ocr.append({"name": name, "text": text, "id": id, "idpage": idpage})
        domain = Domain([], metas=[StringVariable("name"), StringVariable("text"), StringVariable("id"), StringVariable("idpage")])
        out_data = Table.from_list(domain, [[f["name"], f["text"].replace("-\n","").replace("\n",""), f["id"], f["idpage"]] for f in ocr])
        self.Outputs.text.send(out_data)