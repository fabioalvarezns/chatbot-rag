from tools.data_load_vd import books_load
from tools.qdrant_manager import qdrant_manager
from tools.parameters import Config
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain import PromptTemplate
import openai
import tiktoken
from tools.embeast import embeast

###INIT
open_ai_key = Config.OPENAI_KEY
chat = ChatOpenAI(model="gpt-3.5-turbo-0125",openai_api_key=open_ai_key, temperature=0.5)
sofia_database = qdrant_manager(Config.SOFIA_DEV_URL,Config.SOFIA_DEV_KEY)
openai.api_key = open_ai_key
embed_model = 'text-embedding-ada-002'
#new_book = books_load('KB/fuentes/mundodesofia.pdf',200,50,'El mundo de Sofia','Jostein Gaarder')



def conversation_interface(chat_id, question, last_message, message_number,embeading_model, collection):
    
    if embeading_model == 'openai':
        res = openai.Embedding.create(input=question, engine=embed_model)['data'][0]['embedding']
    
    if embeading_model == 'thenlper/gte-base':
        embedding = embeast('thenlper/gte-base')
        res = embedding.execute(question)

    query = sofia_database.search(res, collection)


    i = 1
    context_list=[]
    for context in query:
        context_dict = {
            f"context_{i}": context.payload['text'],
            f"context_{i}_fuente": context.payload['fuente'],
            f"context_{i}_pagina": context.payload['pagina'],
            f"context_{i}_autor": context.payload['autor'],                                    
        }
        i += 1
        context_list.append(context_dict)

    #3. {context_3} fuente: {context_3_fuente} pagina: {context_3_pagina} autor: {context_3_autor}
    sofia_template = """
    Eres Sofia Admunsen
    Personalidad: 
    Una adolescente con curiosidad intelectual que la lleva a indagar en la lectura para responder 
    preguntas trascendentales.

    Estas leyendo un libro y la siguiente es informacion relacionada, USA SOLO ESTA INFORMACION PARA RESPONDER
    ###
    Informacion libro:
    1. {context_1} fuente: {context_1_fuente} pagina: {context_1_pagina} autor: {context_1_autor}
    2. {context_2} fuente: {context_2_fuente} pagina: {context_2_pagina} autor: {context_2_autor}
    ###
    Debes responder con mensajes creativos que esten basados en tu personalidad y el contexto anterior SOLO si tienen relacion, 
    en caso que no, responde solo lo que te dicen. Siempre en primera persona. NUNCA DIGAS QUE ERES UN MODELO DE LENGUAJE NATURAL.
    DEBES USAR SOLO LA INFORMACION DEL LIBRO PARA RESPONDER
    Ejemplo: 
    Peticion: Quien eres ? 
    Respuesta: Soy Sofia Admunsen, una adolescente con curiosidad intelectual que me lleva a indagar en la filosofia para responder preguntas trascendentales.

    DEBES DAR RESPUESTAS CONCRETAS
    """

    #"context_3","context_3_fuente","context_3_pagina", "context_3_autor"],
    prompt = PromptTemplate(
        input_variables=["context_1","context_1_fuente","context_1_pagina", "context_1_autor",
                        "context_2","context_2_fuente","context_2_pagina", "context_2_autor"],
        template=sofia_template,
    )
    # output = prompt.format(context_1=context_list[0]['context_1'], context_1_fuente=context_list[0]['context_1_fuente'], context_1_pagina=context_list[0]['context_1_pagina'], context_1_autor=context_list[0]['context_1_autor'], 
    #                        context_2=context_list[1]['context_2'], context_2_fuente=context_list[1]['context_2_fuente'], context_2_pagina=context_list[1]['context_2_pagina'], context_2_autor=context_list[1]['context_2_autor'],
    #                         context_3=context_list[2]['context_3'], context_3_fuente=context_list[2]['context_3_fuente'], context_3_pagina=context_list[2]['context_3_pagina'], context_3_autor=context_list[2]['context_3_autor'])    


    output = prompt.format(context_1=context_list[0]['context_1'], context_1_fuente=context_list[0]['context_1_fuente'], context_1_pagina=context_list[0]['context_1_pagina'], context_1_autor=context_list[0]['context_1_autor'], 
                            context_2=context_list[1]['context_2'], context_2_fuente=context_list[1]['context_2_fuente'], context_2_pagina=context_list[1]['context_2_pagina'], context_2_autor=context_list[1]['context_2_autor']) 

    print(output)
    messages_pre = [
        SystemMessage(content="Eres Sofia Admusen, una joven con curiosidad inteletual, que siempre responde con respuestas cortas, creativas y divertidas, satira. SIEMPRE RESUME Y CONTESTA PARECIDO AL USUARIO"),
        AIMessage(content=output),
        HumanMessage(content=last_message),
        HumanMessage(content=question),
    ]


    ai_response = chat(messages_pre)

    interaction_len = output + question + ai_response.content + last_message

   

    tokens =  tiktoken.get_encoding('cl100k_base').encode(
                interaction_len,
                disallowed_special=()
            )

    
    
    
    return {
        "chat_id": chat_id,
        "human_message": question,
        "last_message": last_message,
        "message_number": message_number,  
        "ai_response": ai_response.content,
        "tokens": len(tokens),
        "price": len(tokens)*(0.002/1000),
        "currency": "USD"
    }

