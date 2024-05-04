from fastapi import FastAPI, Request
from fastapi.params import Body
from tools.parameters import Config
from tools.history import history
from tools.mongomanager import MongoManager
import httpx
import schema
#from langchain.callbacks.base import CallbackManager
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from conversation_interface import conversation_interface
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

##### INIT
OPEN_AI_KEY = Config.OPENAI_KEY
app = FastAPI()

#chat = ChatOpenAI(openai_api_key=OPEN_AI_KEY, temperature=0.1)

list_messages = [""]

client_mongo = MongoManager().connect()

# with open('prompts/SytemPrompt/System_prompt.txt') as f:
#          system_message = f.read().replace('\n', ' ')
# with open('prompts/conversationPrompts/human_message_1.txt') as f:
#          human_message_1 = f.read().replace('\n', ' ')
# with open('prompts/conversationPrompts/AI_message_1.txt') as f:
#          AI_message_1 = f.read().replace('\n', ' ')
# with open('prompts/conversationPrompts/human_message_2.txt') as f:
#          human_message_2 = f.read().replace('\n', ' ')
# with open('prompts/conversationPrompts/AI_message_2.txt') as f:
#          AI_message_2 = f.read().replace('\n', ' ')
         
# list_messages.append(human_message_1)
# list_messages.append(AI_message_1)
# list_messages.append(human_message_2)
# list_messages.append(AI_message_2)

#         AIMessage(content=list_messages[1]),
#         HumanMessage(content= list_messages[2]),
#         AIMessage(content=list_messages[3]),
#         AIMessage(content=system_message),
#         HumanMessage(content=new_interaction)
#         ]
    
#     return messages
    


        
@app.post('/')
async def generation(message: schema.userMessage): 
        question = message.message    
        #updateListMessages(question)
        
        response = conversation_interface(question=question,last_message=list_messages[0],embeading_model='thenlper/gte-base',collection='books_2')
        #updateListMessages(response["ai_response"])c
        #print(list_messages)
        return {
                "AIResponse": response["ai_response"],
                "tokens": response["tokens"],
                "price": response["price"]
        }

@app.post("/webhook")
async def webhook(request: Request):
    message_telegram = await request.json()
    chat_id = message_telegram["message"]["from"]["id"]
    incoming_message = message_telegram["message"]["text"]
    
    
    collection = client_mongo.sofia_dev.conversations
    
    
    history_object = history(collection,chat_id)
    last_message = history_object.get_last_message()
    
    output_message = conversation_interface(question=incoming_message,last_message=last_message['ai_response'],chat_id=chat_id, \
                                            message_number=last_message['message_number'],embeading_model='thenlper/gte-base',collection='books') 
    history_object.save_new_message(output_message)
    outputMessageChat = {
           "chat_id": chat_id,
           "text": output_message["ai_response"]
    }
        
    url = Config.BOT_URL

    async with httpx.AsyncClient() as client:
           response = await client.post(url=url,json=outputMessageChat)
    
    return message_telegram 