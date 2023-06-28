import openai
from fastapi import FastAPI
import re
from openai.embeddings_utils import get_embedding
from SPARQLWrapper import SPARQLWrapper, JSON

app = FastAPI()


openai.api_key = "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"

@app.post("/corregir_texto")
async def corregir_texto(texto: str):
    texto = texto.replace('\n', ' ')
    # limpiar el texto eliminando caracteres especiales y números
    texto_limpio = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]', ' ', texto)
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
async def find_entities(texto: str):
    LIMIT = 512
    entidades = []
    if len(texto) > LIMIT:
        # Dividir el texto en partes más pequeñas
        partes = re.findall(r'\b\w+\b', texto)
        partes = [partes[i:i+LIMIT] for i in range(0, len(partes), LIMIT)]
        partes = [' '.join(p) for p in partes]

        # Analizar cada parte por separado y concatenar los resultados
        resultados = []
        for parte in partes:
            res = openai.Completion.create(
                engine='text-davinci-002',
                prompt=f"Sacame las entidades del siguiente texto como una lista: \"{parte}\"",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            resultados.append(res.choices[0].text)
        resultado_completo = ' '.join(resultados)
    else:
        # Analizar el texto completo
        res = openai.Completion.create(
            engine='text-davinci-002',
            prompt=f"Sacame las entidades del siguiente texto como una lista: \"{texto}\"",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        resultado_completo = res.choices[0].text

    # Procesar el resultado para extraer las entidades
    entidades = []
    for linea in resultado_completo.splitlines():
        if len(linea) > 0:
            entidades.append(linea)
    # Retornar las entidades encontradas
    return {"entidades": entidades}

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

    # Dividir la palabra recibida si contiene más de una palabra
    palabras = term.split()

    # Lista de términos a excluir
    terminos_excluidos = ["el", "la", "los", "las", "del", "al", "un", "una", "de", "a", "del"]

    # Escapar caracteres especiales en cada palabra de búsqueda
    palabras = [palabra for palabra in palabras if palabra.lower() not in terminos_excluidos]

    uris = []

    # Buscar cada palabra individualmente en DBpedia
    for palabra in palabras:
        # Definir la consulta SPARQL para buscar la palabra en español
        palabra = palabra.capitalize()
        query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?s
            WHERE {{
                ?s rdfs:label "{palabra}"@es .
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
            uris.append(uri)

    if len(uris) > 0:
        return {"uris": uris}
    else:
        return {"uris": None}
