import openai
from transformers import AutoTokenizer, AutoModel
import os 
from dotenv import load_dotenv, find_dotenv

class embeast(): 

    load_dotenv(find_dotenv())

    __available_models = ["openai","thenlper/gte-base"]

    __models = {
        "openai": {
            "model": "text-embedding-ada-002",
            "function": "openai_execute"
        }, 
        "thenlper/gte-base": {
            "model": "thenlper/gte-base",
            "function": "thenlper_execute"
        }
    }

    def __init__(self, model) -> None:
        
        if model in embeast.__available_models:
            self.model = model 
        else: 
            raise ValueError(f"The model: {model}, is not available yet")
        
        if "OPENAI_API_KEY" in os.environ:
            self.api_key = os.environ['OPENAI_API_KEY']

           
    def execute(self, query):
        result = self.__routing(query,self.model)
        
        return result
    
    
    def __routing(self, query: str, model: str) -> list:
        
        model_name = self.__models[f"{model}"]["model"]

        if self.__models[f"{model}"]["function"] == "openai_execute":
            
            result = self.__openai_execute(query, model_name)

        if self.__models[f"{model}"]["function"] == "thenlper_execute":
            
            result = self.__thenlper_execute(query)
        
        return result  
    
    
    def __openai_execute(self, query: str, model_name: str) -> list: 
       
       openai.api_key = self.api_key
       
       response = openai.embeddings.create(
                            input=query,
                            model=model_name
                                )
       embeddings = response.data[0].embedding

     
       return embeddings
    
    
    def __hf_initializer(self): 
        hf_tokenizer = AutoTokenizer.from_pretrained(self.model)
        hf_model = AutoModel.from_pretrained(self.model)

        return hf_model,hf_tokenizer

    
    
    def __thenlper_execute(self,query: str) -> list: 
        
        hf_model, hf_tokenizer = self.__hf_initializer()
        
        batch_dict = hf_tokenizer([query.strip().lower()], max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = hf_model(**batch_dict)
        last_hidden = outputs.last_hidden_state.masked_fill(~batch_dict['attention_mask'][..., None].bool(), 0.0)
        torch_embeddings_list = last_hidden.sum(dim=1) / batch_dict['attention_mask'].sum(dim=1)[..., None]
        return torch_embeddings_list[0].tolist() # dimension of 768
        

        
