from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.document_loaders import PyMuPDFLoader
import os 
from fastapi import HTTPException,status,File 
class Spliter():
    def __init__(self):
        self.chunker=RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
    
    def create_chunks(self,doc:File):
        try:
            if not doc.filename:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error: file name is missing"
                )

            file_name=os.path.basename(doc.filename)
            file_path=f"media/{file_name}"
            os.makedirs("media", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(doc.file.read())
            
            doc_loader=PyMuPDFLoader(file_path)
            docs=doc_loader.load()
            chunks=self.chunker.split_documents(docs)
            return chunks
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )