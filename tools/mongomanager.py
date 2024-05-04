from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import PrettyPrinter
from dotenv import load_dotenv, find_dotenv
import os 



class MongoManager(): 
    
    
    printer = PrettyPrinter()
    load_dotenv(find_dotenv())

    

    def __init__(self) -> None:
        
        self.__username = os.environ['MONGODB_USER']
        self.__password = os.environ['MONGO_DB_PASSWORD']
        self.__cluster_name = os.environ['MONGODB_CLUSTER_NAME']
        self.__uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster_name}.pmrntt9.mongodb.net/?retryWrites=true&w=majority"

        self.client = MongoClient(self.__uri, server_api=ServerApi('1'))


    def connect(self): 
        return self.client
    
    def last_message(collection, conversation_id): 
        

        result_pre = list(collection.aggregate(
                    [
                        
                        {"$match": {"chat_id": conversation_id}},
                        
                        {
                            "$group": {
                                "_id": "$chat_id",
                                "maxNumeroConversacion": {"$max": "$message_number"}
                            }
                        }
                        ]
                        ))
        
        if result_pre:
            result_pre = result_pre[0]
            final_result = list(collection.aggregate(
                [
                    {"$match": {"$and": [{"chat_id": result_pre['_id']}, {"message_number": result_pre['maxNumeroConversacion']}]}}
                ]
            ))
        
            return final_result[0]
        
        else: 
            return 'Not finded'
    
    def save_message(collection, message): 
        
        try: 
            collection.insert_one(message)
        except Exception as e:
            raise e
        
    



         
        