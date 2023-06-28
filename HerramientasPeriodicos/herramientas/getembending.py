from Orange.widgets.widget import OWWidget, Input, Output
from Orange.data import Table, Domain, StringVariable
import httpx
import re

class GetEmbending(OWWidget):
    name = "GetEmbending"
    description = "Obtener Embeddings de un Texto"
    icon = "icons/embending.svg"
    priority = 10

    class Outputs:
        periodicosComple = Output("PeriodicosComple", Table)
    
    class Inputs:
        periodicos = Input("Periodicos", Table)
    
    def __init__(self):
        super().__init__()

    @Inputs.periodicos
    def set_periodicos(self, periodicos):
        if periodicos is not None:
            self.periodicos = periodicos
            self.getEmbeddings()
        else:
            self.periodicos = None
            self.Outputs.periodicosComple.send(self.periodicos)

    def getEmbeddings(self):
        url = "http://127.0.0.1:8000/get_embedding?text="
        embeddings = []
        textoembending = []
        for row in self.periodicos:
            embeddings = []
            name = row["name"]
            texto = row["text"].value
            id2 = row["id"]
            id_page = row["idpage"]
            entidades = row["entidades"]
            texto = texto.replace("\n", "")
            texto = texto.replace("\\n", "")
            patron = r'[\'\"\n:{}\[\].,]'
            texto = re.sub(patron, '', texto)
            # Enviar solicitud HTTP POST con el texto a corregir
            response = httpx.post(url+texto, timeout=420)
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
               result = response.json()
               if isinstance(result, list):
                embeddings.append(result)
               else:
                    embeddings.append(result) 
            else:
                print("Error en la solicitud.")
            textoembending.append({
                "name": name, 
                "text": texto, 
                "entidades": entidades, 
                "id": id2, 
                "id_page": id_page,
                "embedding": str(embeddings),
                })
        
        salida = [{"name": ent1["name"], "text": ent1["text"], "entidades": ent1["entidades"], "id": ent1["id"], "idpage": ent1["id_page"], "embending":ent1["embedding"]} for ent1 in textoembending]
        domain = Domain([],metas=[StringVariable("name"), StringVariable("text"), StringVariable("entidades"), StringVariable("id"), StringVariable("idpage"), StringVariable("embending")])
        out_data= Table.from_list(domain, [[f["name"], f["text"], f["entidades"], f["id"], f["idpage"], f["embending"]] for f in salida])
        self.Outputs.periodicosComple.send(out_data)