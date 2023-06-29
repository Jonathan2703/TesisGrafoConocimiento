from Orange.widgets.widget import OWWidget, Input, Output
from Orange.data import Table, Domain, StringVariable
import httpx
import json
class ReconocimientoEntidates(OWWidget):
    name = "ReconocimientoEntidades"
    description = "Reconocimiento de entidades"
    icon = "icons/world.svg"
    priority = 10

    class Outputs:
        periodicos_entidades = Output("Entidades", Table)

    class Inputs:
        textperiodicos = Input("Periodicos", Table)

    def __init__(self):
        super().__init__()

    @Inputs.textperiodicos
    def set_data(self, textperiodicos):
        self.textperiodicos = textperiodicos
        self.find_entity()
        
    
    def find_entity(self):
        url = "http://127.0.0.1:8000/find_entities"
        textos_corregidos = []
        for row in self.textperiodicos:
            name = row["name"]
            texto = row["text"].value
            id2 = row["id"]
            id_page = row["idpage"]
            
            # construir el cuerpo de la solicitud en formato JSON
            body = {"texto": texto}

            # Enviar solicitud HTTP POST con el texto a corregir
            response = httpx.post(url, json=body, timeout=1800)
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                entidades = response.json()["entidades"]
            else:
                # En caso de error, establecer las entidades como una lista vacía
                entidades = []
            
            # Agregar el texto corregido y las entidades a la lista de salida
            textos_corregidos.append({
                "name": name,
                "text": texto,
                "entidades": entidades,
                "id": id2,
                "id_page": id_page,
            })
        
        # crear la lista de salida utilizando la sintaxis de comprensión de listas
        salida = [{"name": ent1["name"], "text": ent1["text"], "entidades": ent1["entidades"], "id": ent1["id"], "idpage": ent1["id_page"]} for ent1 in textos_corregidos]
        
        # enviar la lista de salida a través de la conexión de salida
        domain = Domain([], metas=[StringVariable("name"), StringVariable("text"),StringVariable("entidades"), StringVariable("id"), StringVariable("idpage")])
        out_data = Table.from_list(domain, [[f["name"], f["text"], f["entidades"], f["id"], f["idpage"]] for f in salida])
        self.Outputs.periodicos_entidades.send(out_data)