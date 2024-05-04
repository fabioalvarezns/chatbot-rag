# chatbot_rag

Chatbot usando los modelos de OPENAI, con una tecnica que se llama RAG la cual te permite inyectar informacion al LLM que no fue usada en su entrenamiento, puedes pasar cualquier tipo de informacion de text. Para este demo tomamos el pdf de un libro llamada "El mundo de Sofia" con el cual le inyectamos informacion al LLM para que responda con información del libro y tenga la personalidad de la protagonista del libro.

La busqueda en este caso es por simaliridad semantica, lo que se hace es convertir el texto a vectores y usar esos vectores para calcular la distancia entre la pregunta del usario y la informacion guardada en vectores, los vectores mas cercanos 

# Load data to vector database. 

El primer paso es procesar y cargar el texto, eso lo pueden ver en el load_data.py, y tienen una clase llamada qdrant_manager.py que les pertmite gestionar todo lo de la base de datos. 

Deben crear primero una cuenta en qdrant y obtener el api key. 

el .env del repo es el siguiente:

OPENAI_KEY= "sk-"
SOFIA_DEV_KEY="vG33"
SOFIA_DEV_URL="<URL DE LA BASE DE DATOS >"
BOT_URL="< URL DEL BOT QUE SE CREA CON TELEGRAM >"
MONGODB_USER=<mongo user> -> En caso de usar mongodb para gaurdar la información. 
MONGO_DB_PASSWORD=<mongo password> 
MONGODB_CLUSTER_NAME=<mongo cluster name> 


# TOOLS 

1. Embeast: clase que te permite crear vectores a partir de un texto.
2. qrant_manager: clase que te permite manajar todo lo que tiene que ver con la base de datos de vectores, puedes crear colecciones subir informacion y mas.
3. mongomanager: clase que te permite manejar todo lo relacionado a mongodb.
4. conversation_interface: clase que gestionas todas las interacciones del chatbot.


para instalar los requirements.txt 

```
pip install -r requirements.txt
```
