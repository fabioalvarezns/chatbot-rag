from tools.mongomanager import MongoManager

class history(): 

    def __init__(self, collection, conversation_id: str ) -> None:
        self.conversation_id = conversation_id
        self.collection = collection

        
        

    def get_last_message(self): 
        
        response = MongoManager.last_message(self.collection,self.conversation_id) 

        

        if response == 'Not finded':
             
             return {
                 'ai_response': '',
                 'message_number': 0,
                 
             }
        
        else: 
            
            return response
        

    def save_new_message(self, new_message): 
        
        
        new_message['message_number'] = new_message['message_number'] + 1
        
        MongoManager.save_message(self.collection,new_message)
        