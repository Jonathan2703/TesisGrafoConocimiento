from Orange.widgets.widget import OWWidget, Output
from Orange.widgets import gui
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
import requests
from bs4 import BeautifulSoup
import base64 
from Orange.data import Table, Domain, StringVariable

class PDFDownloaderWidget(OWWidget):
    name = "Data Sampler"  
    description = "Randomly selects a subset of instances from the data set"  
    icon = "icons/DataSamplerA.svg" 
    priority = 10 

    class Outputs:
        out_data = Output("Data", Table)
        meta_data = Output("MetaData", Table)

    def __init__(self):
        super().__init__()

        # Set up the internal state
        self.url = "http://repositorio.casadelacultura.gob.ec/oai/request"
        self.max_count = 2
        self.download_all = False
        self.registry = MetadataRegistry()
        self.registry.registerReader("oai_dc", oai_dc_reader)
        self.client = Client(self.url, self.registry)

        # Set up the user interface
        self.url_edit = gui.lineEdit(self.controlArea, self, "url", "Repository URL:")
        self.max_count_spin = gui.spin(self.controlArea, self, "max_count", 1, 100, 1)
        self.download_all_cbx = gui.checkBox(
            self.controlArea, self, "download_all", "Download All Files"
        )
        self.download_button = gui.button(
            self.controlArea, self, "Download Files", callback=self.download_files
        )

    def download_files(self):
        records = self.client.listRecords(
            metadataPrefix="oai_dc", set="col_34000_1534"
        )
        n = 0
        count = 0
        metadata_list = []
        files = []
        for val in records:
            url_pdf = (
                "http://repositorio.casadelacultura.gob.ec/handle/"
                + str(val[0].identifier()).split(":")[-1]
            )
            html = get_html(url_pdf)
            soup = BeautifulSoup(html, "html.parser")
            meta = soup.find_all("meta")

            metadata_dict = {}
            for m in meta:
                if m.has_attr("name"):
                    metadata_dict[m["name"]] = m.get("content")
            metadata_dict['id'] = str(val[0].identifier()).split(":")[-1]
            metadata_list.append(metadata_dict)

            for a in meta:
                if "citation_pdf_url" in str(a):
                    archivo = a["content"]
                    if "http://" in archivo:
                        n += 1
                        response = requests.get(archivo)
                        encoded_file = base64.b64encode(response.content).decode("utf-8")
                        files.append({'name': archivo.split("/")[-1], 'content': encoded_file, 'id': str(val[0].identifier()).split(":")[-1]})
                        count += 1
                        if count >= self.max_count:
                            break
            if count >= self.max_count:
                break
        domain = Domain([], metas=[StringVariable("name"), StringVariable("content"), StringVariable("id")])
        out_data = Table.from_list(domain, [[f["name"], f["content"], f["id"]] for f in files])
        self.Outputs.out_data.send(out_data)
        domain_metadata = Domain([], metas=[StringVariable("Generator"), StringVariable("viewport"), StringVariable("DCTERMS.dateAccepted"), StringVariable("DCTERMS.available"), StringVariable("DCTERMS.issued"), StringVariable("DC.identifier"), StringVariable("DCTERMS.abstract"), StringVariable("DCTERMS.extent"), StringVariable("DC.language"), StringVariable("DC.publisher"), StringVariable("DC.subject"), StringVariable("DC.title"), StringVariable("DC.type"), StringVariable("citation_keywords"), StringVariable("citation_title"), StringVariable("citation_publisher"), StringVariable("citation_language"), StringVariable("citation_pdf_url"), StringVariable("citation_date"), StringVariable("citation_abstract_html_url"), StringVariable("id")])
        out_metadata = Table.from_list(domain_metadata, [[f.get("Generator", ""), f.get("viewport", ""), f.get("DCTERMS.dateAccepted", ""),f.get("DCTERMS.available", ""), f.get("DCTERMS.issued", ""), f.get("DC.identifier", ""), f.get("DCTERMS.abstract", ""), f.get("DCTERMS.extent", ""), f.get("DC.language", ""), f.get("DC.publisher", ""), f.get("DC.subject", ""), f.get("DC.title", ""), f.get("DC.type", ""), f.get("citation_keywords", ""), f.get("citation_title", ""), f.get("citation_publisher", ""), f.get("citation_language", ""), f.get("citation_pdf_url", ""), f.get("citation_date", ""), f.get("citation_abstract_html_url", ""), f.get("id", "")] for f in metadata_list])
        self.Outputs.meta_data.send(out_metadata)


def get_html(url):
    r = requests.get(url)
    return r.content