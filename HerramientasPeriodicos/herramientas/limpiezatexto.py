from Orange.widgets.widget import OWWidget, Input, Output
from Orange.data import Table, Domain, StringVariable
import httpx

class LimpiezaTexto(OWWidget):
    name = "Limpiador de Texto"
    description = "Limpia texto de caracteres especiales"
    icon = "icons/ia.svg"
    priority = 10

    class Outputs:
        output_texto_corregido = Output("Texto", Table)
    
    class Inputs:
        inputtext = Input("Data", Table)

    
    def __init__(self):
        super().__init__()

    @Inputs.inputtext
    def set_data(self, inputtext):
        self.inputtext = inputtext
        self.texto_corregido()

    def texto_corregido(self):
        # lista para almacenar los textos corregidos
        textos_corregidos = []
        # procesar cada entrada de texto en self.inputtext
        for entrada in self.inputtext:
            nombre = entrada["name"]
            texto_original = entrada["text"].value
            id = entrada["id"]
            idpage = entrada["idpage"]
            
            # enviar la solicitud POST al endpoint /corregir_texto
            response = httpx.post("http://127.0.0.1:8000/corregir_texto?texto=" + texto_original, timeout=420 )
            if response.status_code == 200:
                texto_corregido = response.json()["texto_corregido"]
            else:
                print("Error en la solicitud POST")
                # manejar el error de la solicitud POST
                texto_corregido = ""
            
            # agregar el texto corregido a la lista de textos corregidos
            textos_corregidos.append({
                "name": nombre,
                "text": texto_corregido,
                "id": id,
                "idpage": idpage
            })
        # crear la lista de salida utilizando la sintaxis de comprensión de listas
        salida = [{"name": entrada["name"], "text": entrada["text"],"id": id, "idpage": idpage} for entrada in textos_corregidos]

        # enviar la lista de salida a través de la conexión de salida
        domain = Domain([], metas=[StringVariable("name"), StringVariable("text"), StringVariable("id"), StringVariable("idpage")])
        out_data = Table.from_list(domain, [[f["name"], f["text"], f["id"], f["idpage"]] for f in salida])
        self.Outputs.output_texto_corregido.send(out_data)