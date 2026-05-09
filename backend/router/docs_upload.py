from service.vectorDB import Vectorstore
from fastapi import HTTPException,status
from fastapi import APIRouter,File,UploadFile
from service.chunker import Spliter

router=APIRouter()
class Doc_upload(Vectorstore):
    def  __init__(self):
        super().__init__() 
    
    def upload_doc(self,doc_chunks):
        if self.DB ==None:
            self.createDB(doc_chunks)
            return{
                "message":"database create successfully !"
            }
        else:
            try:
                ids_of_chunks=self.DB.add_documents(doc_chunks)
                return{
                    "message":"data added succesfully "
                }
            except Exception as e :
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error: {e}")

upload=Doc_upload()
@router.post("/upload_docs")
def doc_upload(file:UploadFile=File(...)):
    try:
        chunks=Spliter().create_chunks(file)
        return upload.upload_doc(chunks)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"error : {e}")