from Orange.widgets.widget import OWWidget, Input, Output
from Orange.data import Table, Domain, StringVariable
import httpx
import re
class EmparejarDB(OWWidget):
    name = "EmparejarDB"
    description = "Emparejar en DBpedia"
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
        url = "http://127.0.0.1:8000/search/"
        textoembending = []
        for row in self.periodicos:
            name = row["name"]
            text = row["text"]
            entidades=row["entidades"]
            id=row["id"]
            idpage=row["idpage"]
            embending=row["embending"]
            generator=row["Generator"]
            viewport=row["viewport"]
            dta=row["DCTERMS.dateAccepted"]
            dta2=row["DCTERMS.available"]
            iss=row["DCTERMS.issued"]
            identifier=row["DC.identifier"]
            abs=row["DCTERMS.abstract"]
            ext=row["DCTERMS.extent"]
            lan=row["DC.language"]
            pub=row["DC.publisher"]
            sub=row["DC.subject"]
            tit=row["DC.title"]
            typ=row["DC.type"]
            keyw=row["citation_keywords"]
            cit_tit=row["citation_title"]
            cit_pub=row["citation_publisher"]
            cit_lan=row["citation_language"]
            cit_pdf=row["citation_pdf_url"]
            cit_dat=row["citation_date"]
            cit_abs=row["citation_abstract_html_url"]
            new_keys=[]
            for i in str(entidades).split(","):
                if i!="":
                    response = httpx.get(url+(str(i).strip()), timeout=420)
                    if response.status_code == 200:
                        result=response.json()
                        if result['uri']!=None:
                            new_keys.append(result['uri'])
                        else:
                            print("isnone")
                            new_keys.append(i)
                    else:
                        new_keys.append(i)
                        print("Error en la solicitud.")
            new_keys_str=""
            first=True
            for i in new_keys:
                if first==True:
                    first=False
                else:
                    new_keys_str=new_keys_str+","
                new_keys_str=new_keys_str+i
            textoembending.append({
                "name": name, 
                "text": text, 
                "entidades": new_keys_str, 
                "id": id, 
                "idpage": idpage,
                "embending": embending,
                "Generator":generator,
                "viewport":viewport,
                "DCTERMS.dateAccepted":dta,
                "DCTERMS.available":dta2,
                "DCTERMS.issued":iss,
                "DC.identifier":identifier,
                "DCTERMS.abstract":abs,
                "DCTERMS.extent":ext,
                "DC.language":lan,
                "DC.publisher":pub,
                "DC.subject":sub,
                "DC.title":tit,
                "DC.type":typ,
                "citation_keywords":keyw,
                "citation_title":cit_tit,
                "citation_publisher":cit_pub,
                "citation_language":cit_lan,
                "citation_pdf_url":cit_pdf,
                "citation_date":cit_dat,
                "citation_abstract_html_url":cit_abs,
                })
        salida = [{
                "name": ent1["name"], 
                "text": ent1["text"], 
                "entidades": ent1["entidades"], 
                "id": ent1["id"], 
                "idpage": ent1["idpage"],
                "embending": ent1["embending"],
                "Generator":ent1["Generator"],
                "viewport":ent1["viewport"],
                "DCTERMS.dateAccepted":ent1["DCTERMS.dateAccepted"],
                "DCTERMS.available":ent1["DCTERMS.available"],
                "DCTERMS.issued":ent1["DCTERMS.issued"],
                "DC.identifier":ent1["DC.identifier"],
                "DCTERMS.abstract":ent1["DCTERMS.abstract"],
                "DCTERMS.extent":ent1["DCTERMS.extent"],
                "DC.language":ent1["DC.language"],
                "DC.publisher":ent1["DC.publisher"],
                "DC.subject":ent1["DC.subject"],
                "DC.title":ent1["DC.title"],
                "DC.type":ent1["DC.type"],
                "citation_keywords":ent1["citation_keywords"],
                "citation_title":ent1["citation_title"],
                "citation_publisher":ent1["citation_publisher"],
                "citation_language":ent1["citation_language"],
                "citation_pdf_url":ent1["citation_pdf_url"],
                "citation_date":ent1["citation_date"],
                "citation_abstract_html_url":ent1["citation_abstract_html_url"],
                } for ent1 in textoembending]
        domain = Domain([],metas=[StringVariable("name"), 
                                  StringVariable("text"), 
                                  StringVariable("entidades"), 
                                  StringVariable("id"), 
                                  StringVariable("idpage"), 
                                  StringVariable("embending"),
                                  StringVariable("Generator"),
                                  StringVariable("viewport"),
                                  StringVariable("DCTERMS.dateAccepted"),
                                  StringVariable("DCTERMS.available"),
                                  StringVariable("DCTERMS.issued"),
                                  StringVariable("DC.identifier"),
                                  StringVariable("DCTERMS.abstract"),
                                  StringVariable("DCTERMS.extent"),
                                  StringVariable("DC.language"),
                                  StringVariable("DC.publisher"),
                                  StringVariable("DC.subject"),
                                  StringVariable("DC.title"),
                                  StringVariable("DC.type"),
                                  StringVariable("citation_keywords"),
                                  StringVariable("citation_title"),
                                  StringVariable("citation_publisher"),
                                  StringVariable("citation_language"),
                                  StringVariable("citation_pdf_url"),
                                  StringVariable("citation_date"),
                                  StringVariable("citation_abstract_html_url"),
                                  ])
        out_data= Table.from_list(domain, [[f["name"], 
                                  f["text"], 
                                  f["entidades"], 
                                  f["id"], 
                                  f["idpage"], 
                                  f["embending"],
                                  f["Generator"],
                                  f["viewport"],
                                  f["DCTERMS.dateAccepted"],
                                  f["DCTERMS.available"],
                                  f["DCTERMS.issued"],
                                  f["DC.identifier"],
                                  f["DCTERMS.abstract"],
                                  f["DCTERMS.extent"],
                                  f["DC.language"],
                                  f["DC.publisher"],
                                  f["DC.subject"],
                                  f["DC.title"],
                                  f["DC.type"],
                                  f["citation_keywords"],
                                  f["citation_title"],
                                  f["citation_publisher"],
                                  f["citation_language"],
                                  f["citation_pdf_url"],
                                  f["citation_date"],
                                  f["citation_abstract_html_url"],
                                  ] for f in salida])
        self.Outputs.periodicosComple.send(out_data)