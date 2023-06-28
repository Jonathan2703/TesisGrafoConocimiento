# Generación de  un grafo de conocimiento de periódicos antiguos del Ecuador a través de procesos OCR.

Este proyecto aborda el desafío de acceder a información histórica almacenada en periódicos antiguos que se encuentran en un estado deteriorado y son difíciles de manejar. Para solucionar este problema, se propone una solución basada en la digitalización de texto, procesamiento de texto y tecnologías de la web semántica.

El objetivo principal es extraer la información de los periódicos antiguos, organizarla de manera estructurada y generar un grafo de conocimiento que represente los eventos históricos en Ecuador durante los siglos XIX y XX. Se automatizan los pasos del proceso utilizando widgets en la plataforma Orange, que realizan tareas específicas como la extracción de información, identificación de entidades y relaciones, obtención de embeddings de palabras y generación del grafo de conocimiento.

Esta solución permite acceder de manera rápida y eficiente a la información histórica relevante, facilitando la investigación y el análisis de los eventos ocurridos en Ecuador en ese período histórico..

## Instalación

## Instalación

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- Orange Data Mining
- OCR Tesseract
- Poppler
- Apache Jena Fuseki

A continuación, sigue estos pasos para configurar el entorno de desarrollo de Python:

1. Crea un entorno de desarrollo de Python utilizando Conda o cualquier otro gestor de entornos virtual. Puedes ejecutar el siguiente comando para crear un nuevo entorno con Conda:

   ```bash
   conda create --name mi_entorno python=3.8
   ```

2. Activa el entorno recién creado. Para Conda, utiliza el siguiente comando:

   ```bash
   conda activate mi_entorno
   ```

3. Descarga el proyecto desde el repositorio y accede al directorio del proyecto.

4. Instala todas las dependencias necesarias ejecutando el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará todas las bibliotecas y herramientas necesarias para ejecutar el proyecto, incluyendo Orange Data Mining, OCR Tesseract y pdf2image.

Después de instalar Orange Data Mining, abre el Orange Command Prompt y escribe la siguiente sentencia:

``` pip install -e ruta/herramientas ```
Una vez completados estos pasos, habrás configurado correctamente el entorno de desarrollo y todas las dependencias necesarias para ejecutar el proyecto.

¡Ahora estás listo para utilizar el proyecto y explorar sus funcionalidades!

## Uso

    Abre Orange Data Mining: Para comenzar, asegúrate de tener Orange Data Mining instalado en tu sistema. Abre la aplicación y espera a que se cargue.

    Accede a los widgets creados: En la barra de herramientas de Orange, encontrarás los widgets que han sido creados para este proyecto. Estos widgets están diseñados para realizar tareas específicas relacionadas con el procesamiento de texto y la generación de un grafo de conocimiento. Arrastra y suelta los widgets en el lienzo de Orange para comenzar a construir tu flujo de trabajo.

    Crea un flujo de trabajo: Utilizando los widgets disponibles, crea un flujo de trabajo que te permita realizar todas las tareas necesarias para extraer la información de los periódicos antiguos, organizarla estructuradamente y generar el grafo de conocimiento. Conecta los widgets en el orden adecuado para asegurar que los datos fluyan de un widget a otro de manera correcta.

    Inicia el servidor de FastAPI: Antes de probar los widgets, debes iniciar el servidor de FastAPI. Abre una terminal o línea de comandos en el directorio del proyecto y ejecuta el siguiente comando: uvicorn server:app. Esto iniciará el servidor y te permitirá interactuar con los widgets a través de una interfaz web.

    Inicia Apache Jena Fuseki y sube la ontología: Para utilizar plenamente los widgets, es necesario iniciar Apache Jena Fuseki, una plataforma para almacenar y consultar datos RDF. Asegúrate de tener Apache Jena Fuseki instalado y configurado correctamente. Inicia el servidor de Fuseki y carga la ontología necesaria para el proyecto.

    Prueba los widgets: Una vez que hayas configurado todo correctamente, puedes comenzar a probar cada uno de los widgets en tu flujo de trabajo. Ajusta los parámetros según sea necesario y ejecuta el flujo para ver los resultados.



## Autor

Raúl Torres, Jonnathan Valdez

## Licencia

Indicación de la licencia bajo la cual se distribuye el proyecto.

