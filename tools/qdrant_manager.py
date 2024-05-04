from qdrant_client import QdrantClient
from qdrant_client.http import models



class qdrant_manager():
    
    def __init__(self,url,api_key) -> None:
        self.url = url
        self.api_key = api_key

        self.qdrant_client = QdrantClient(
            url=self.url, 
            api_key=self.api_key
            )


    def create_collection(self,collection_name: str, vector_size: int):
        try:
            self.qdrant_client.recreate_collection(
            collection_name=f"{collection_name}",
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
                )
        except:
            return{
                "status": "FAIL",
                "collection_name": collection_name,
                "vector_size": vector_size    
            }   
        return{
            "status": "SUCCESS",
            "collection_name": collection_name,  
            "vector_size": vector_size
        }

    def delete_collection(self, collection_name):
        try: 
            self.qdrant_client.delete_collection(collection_name=f"{collection_name}")
        except:
            return{
                "status": "FAIL",
                "collection_name": collection_name    
            }   
        
        return {
                "status": "SUCCESS",
                "collection_name": collection_name    
            }   


    def update_collection_parameters(self,collection_name):
        """
        Under construction, don't use 
        """
        self.qdrant_client.update_collection(
        collection_name=f"{collection_name}",
        optimizer_config=models.OptimizersConfigDiff(
            indexing_threshold=10000
        )
    )

    def collection_info(self,collection_name):
        return self.qdrant_client.get_collection(collection_name=f"{collection_name}")

    def get_collections(self):
        return self.qdrant_client.get_collections()


    def insert_vector_batch(self,collection_name: str,payloads: list, ids: list, vectors: list):
        #print(len(payloads))
        output = self.qdrant_client.upsert(
            collection_name=f"{collection_name}",
            points=models.Batch(
                    ids=ids,
                    payloads=payloads,
                    vectors=vectors
        )
            )
        
        return output

    def search(self, vector, collection):
        a = self.qdrant_client.search(
        collection_name=collection,
        search_params=models.SearchParams(
            hnsw_ef=128,
            exact=False
        ),
        query_vector=vector,
        limit=3,
        )
        
        return a

    