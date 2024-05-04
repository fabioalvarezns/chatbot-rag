import tiktoken
import uuid
import openai
from .qdrant_manager import qdrant_manager
from tools.parameters import Config
from langchain_community.document_loaders import PyPDFLoader
#from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
import hashlib
import json
from time import sleep
from tools.embeast import embeast



class books_load():
    def __init__(self,file_source, chunk_size, overlap, fuente, autor, open_ai_key): 
        self.file_source = file_source
        self.chunk_size = chunk_size
        self.overlap= overlap
        self.fuente=fuente
        self.autor = autor
        self.tokenizer = tiktoken.get_encoding('cl100k_base')
        self.embed_model = "text-embedding-ada-002"
        self.open_ai_key = open_ai_key
        self.sofia_db = qdrant_manager(Config.SOFIA_DEV_URL,Config.SOFIA_DEV_KEY)

    def tiktoken_len(self,text):
        """
        Function that estimate the number of tokens
        """
        tokens =  self.tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)

    # def textLoader(self,path):
    #     """
    #     Load data from TXT file 
    #     """
    #     loader = TextLoader(path)
    #     data = loader.load()
    #     return data[0].page_content


    def pdfLoader(self,path):
        """
        Load data from PDF file 
        """
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        return pages

    def hashsingId(self,data, id):
        """
        making the ids with using hash
        """
        m = hashlib.md5()
        hash = data.metadata['source'] + str(data.metadata['page'])
        m.update(hash.encode('utf-8'))
        uid = m.hexdigest()[:12]
        data_id = f'{uid}-{id}'
        uuid_generado = uuid.uuid5(uuid.NAMESPACE_DNS, data_id)
        return str(uuid_generado)

    def chunkSplitter(self,chunksize,overlap,data):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunksize,
            chunk_overlap=overlap,  # number of tokens overlap between chunks
            length_function=self.tiktoken_len,
            separators=['\n\n', '\n', ' ', '']
            )

        chunks = text_splitter.split_text(data)
        return chunks

    def saveDataset(self,documents,name):
        with open(f'KB/datasets/{name}-clean.jsonl', 'w', encoding='utf-8') as f:
            for doc in documents:
                f.write(json.dumps(doc,ensure_ascii=False)+ '\n')
        return f'KB/datasets/{name}-clean.jsonl'


    def prepare_data(self,dataset_name):
        """
        Cleaning data to make the embeddings and load to qdrant
        """
        
        documents = []
        file_source = f"{self.file_source}"
        data = self.pdfLoader(file_source)
      
        for doc in data: 
            chunks = self.chunkSplitter(self.chunk_size,self.overlap,doc.page_content)
            for i,chunk in enumerate(chunks):
                documents.append({
                                    "id": self.hashsingId(doc,i),
                                    "text": chunk.replace('\n',' '),
                                    "fuente": self.fuente,
                                    "Autor": self.autor,
                                    "pagina": (int(doc.metadata['page']) + 1)
                                })
        output_path = self.saveDataset(documents,dataset_name)
        return {
            "status": "SUCCESS",
            "book": self.fuente,
            "output_path": output_path,
            "data": documents
        }


    def embbedings(self, texts, model):
        """
        Create embeddings based on a list of texts 
        """
        
        if model == 'openai':
        
            openai.api_key = self.open_ai_key
            embed_model = self.embed_model
            try:
                res = openai.Embedding.create(input=texts, engine=embed_model)
            except:
                done = False
                while not done:
                    sleep(5)
                    try:
                        res = openai.Embedding.create(input=texts, engine=embed_model)
                        done = True
                    except:
                        pass 
            embeds = [record['embedding'] for record in res['data']]
            return embeds
        
        if model == 'thenlper/gte-base':
            embedding_object = embeast('thenlper/gte-base')

            print('empezando a crear embeddings...')
            embeds = [embedding_object.execute(text) for text in texts]
            
            return embeds
        
    
    def load_data(self,batch_size, data, collection_name):
        
        batch_size = batch_size
        for i in range(0,len(data),batch_size):
            i_end = min(len(data),i+batch_size)
            meta_batch = data[i:i_end]
            #ids 
            ids_batch = [x["id"] for x in meta_batch]
            # text to encode
            text_batch = [x['text'] for x in meta_batch]
            #create embeddings 
            embeds = self.embbedings(text_batch, 'thenlper/gte-base')
            #payloads 
            payloads = [
                {
                    'text': x['text'],
                    'fuente': x['fuente'],
                    'autor': x['Autor'],
                    'pagina': x['pagina']
                } for x in meta_batch]
            #print(embeds[0])
            #try: 
                #exists = self.sofia_db.collection_info(collection_name)
                
                #if exists: 
            a = self.sofia_db.insert_vector_batch(collection_name, payloads,ids_batch, embeds)
            print(a)
            # except:
            #     try: 
            #         self.sofia_db.create_collection(collection_name,len(embeds[0]))
            #         #self.sofia_db.insert_vector_batch(collection_name, payloads,ids_batch, embeds)
            #     except: 
            #         print(len(embeds[0]))
            #         return "Error creando coleccion"
                    

        return {
            "status": "SUCCEED",
            "message": f"load data in {collection_name}"
        }        

            

            
             
         

    


