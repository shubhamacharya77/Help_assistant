from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi import HTTPException,status
from functools import lru_cache

@lru_cache(maxsize=1)
def get_vectorstore():
    return Vectorstore()


class Vectorstore():
    def __init__(self):
        self.embedding_model=None
        self.DB=None

    def _get_embedding_model(self):
        if self.embedding_model is None:
            self.embedding_model=HuggingFaceEmbeddings(
                model_name="google/embeddinggemma-300m",
            )
        return self.embedding_model

    def _load_db(self):
        try:
            return Chroma(
                persist_directory="ChromaDB",
                embedding_function=self._get_embedding_model(),
            )
        except Exception:
            return None

    def createDB(self,chunks):
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="error : no chunks provided"
            )

        if isinstance(chunks[0],str):
            try:
                self.DB=Chroma.from_texts(
                texts=chunks,
                embedding=self._get_embedding_model(),
                persist_directory="ChromaDB")
                self.DB.persist()
                return{
            "message":"database created !"
        }
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error :{e}")
        else: 
            try:
                self.DB=Chroma.from_documents(
                documents=chunks,
                embedding=self._get_embedding_model(),
                persist_directory="ChromaDB")
                self.DB.persist()
                return{"message":"database created !"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error :{e}")


    def query_search(self,user_query):
        try:
            if self.DB is None:
                self.DB=self._load_db()
            if self.DB is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="error : create data base first")
            relevantChunks=self.DB.similarity_search(query=user_query,k=3)
            return relevantChunks

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error :{e}")
    

    #call only whene database is already created !
    def add_query(self,user_query):
        if self.DB is None:
            self.DB=self._load_db()

        if self.DB !=None:
            try:
                texts=[user_query] if isinstance(user_query,str) else user_query
                id_of_stored_ticket=self.DB.add_texts(texts)
                return{
                "message":f"ticket stored {id_of_stored_ticket}"
            }
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error : {e}")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error : create data base first ")
