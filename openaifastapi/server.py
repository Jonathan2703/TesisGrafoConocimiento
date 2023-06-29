import openai
from fastapi import FastAPI
import re
from openai.embeddings_utils import get_embedding
from SPARQLWrapper import SPARQLWrapper, JSON
from pydantic import BaseModel

app = FastAPI()

class TextoEntrada(BaseModel):
    texto: str

openai.api_key = "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"


@app.post("/corregir_texto")
async def corregir_texto(texto_entrada: TextoEntrada):
    texto = texto_entrada.texto
    texto = texto.replace('\n', ' ')
    # limpiar el texto eliminando caracteres especiales y números
    texto_limpio = re.sub('[^a-zA-Záéíóú  ÁÉÍÓÚñÑüÜ\s]', ' ', texto)
    texto_limpio = texto_limpio.lower()
    
    maxTokens = 16000
    
    # verificar si el texto original es más largo que el límite de OpenAI
    if len(texto_limpio) > maxTokens:
        # dividir el texto en partes de 2048 caracteres
        partes = [texto_limpio[i:i+maxTokens] for i in range(0, len(texto_limpio), maxTokens)]
        
        # corregir cada parte del texto
        partes_corregidas = []
        for parte in partes:
            correccion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Corrigue el texto, el mismo es obtenido por un proceso ocr de periodicos antiguos del Ecuador, devuelve solo el texto corregido:"},
                    {"role": "assistant", "content": parte}
                ]
            )
            
            respuesta = correccion.choices[0].message["content"]
            partes_corregidas.append(respuesta)
            
        # unir las partes del texto corregido en una sola variable
        texto_corregido = " ".join(partes_corregidas)
    else:
        # corregir el texto original

        correccion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Corrigue el texto, el mismo es obtenido por un proceso ocr de periodicos antiguos del Ecuador, devuelve solo el texto corregido:"},
                {"role": "assistant", "content": texto_limpio}
            ], 
            timeout=1800
        )
        
        texto_corregido = correccion.choices[0].message["content"]
    
    return {"texto_corregido": texto_corregido}



@app.post("/find_entities")
async def find_entities(texto_entrada: TextoEntrada):
    texto = texto_entrada.texto
    maxTokens = 16000
    
    # verificar si el texto original es más largo que el límite de OpenAI
    if len(texto) > maxTokens:
        # dividir el texto en partes de 2048 caracteres
        partes = [texto[i:i+maxTokens] for i in range(0, len(texto), maxTokens)]
        
        # corregir cada parte del texto
        entidades = []
        for parte in partes:
            correccion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Sacame las entidades de este texto, y devuelveme solo las entidades separadas por una coma porfavor:"},
                    {"role": "assistant", "content": parte}
                ]
            )
            
            respuesta = correccion.choices[0].message["content"]
            entidades.append(respuesta)
            
        # unir las partes del texto corregido en una sola variable
        entidades_sacadas = " ".join(entidades)
    else:
        # corregir el texto original

        correccion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Sacame las entidades de este texto, y devuelveme solo las entidades separadas por una coma porfavor:"},
                {"role": "assistant", "content": texto}
            ], 
            timeout=1800
        )
        
        entidades_sacadas = correccion.choices[0].message["content"]
    
    return {"entidades": entidades_sacadas}

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", "")
    text = text.replace("\\n", "")
    text = quitar_caracteres_especiales(text)
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

def quitar_caracteres_especiales(texto):
    patron = r'[\'\"\n:{}\[\].,]'
    texto_limpio = re.sub(patron, '', texto)
    return texto_limpio

@app.post("/get_embedding")
def get_embedding_endpoint(text: str):
    text = text.replace("\n", "")
    text = text.replace("\\n", "")
    text = quitar_caracteres_especiales(text)
    # Set the maximum length of each section to 1048 characters
    max_length = 1048
    if len(text) > max_length:
        sections = [text[i:i+1048] for i in range(0, len(text), 1048)]
        result = []
        for section in sections:
            embedding = get_embedding(section)
            result.append({"text": section, "embedding": embedding})
        return str(result)
    else:
        embedding = get_embedding(text)
        result = {"text": text, "embedding": embedding}
        return result

from urllib.parse import quote

@app.get("/search/{term}")
def search_term(term: str):
    # Establecer el punto final de DBpedia en español
    sparql = SPARQLWrapper("https://es.dbpedia.org/sparql")

    # Capitalizar la primera letra del término de búsqueda
    term = term.capitalize()

    # Escapar caracteres especiales en el término de búsqueda
    term = term.replace("'", "\\'")

    # Definir la consulta SPARQL para buscar el término en español
    query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?s
        WHERE {{
            ?s rdfs:label "{term}"@es .
        }}
        LIMIT 1
    """

    # Establecer la consulta SPARQL
    sparql.setQuery(query)

    # Especificar que el resultado de la consulta sea en formato JSON
    sparql.setReturnFormat(JSON)

    # Ejecutar la consulta y obtener los resultados
    results = sparql.query().convert()

    # Procesar los resultados y obtener la URI del primer resultado
    if "results" in results and "bindings" in results["results"] and len(results["results"]["bindings"]) > 0:
        uri = results["results"]["bindings"][0]["s"]["value"]
        return {"uri": uri}
    else:
        return {"uri": None}