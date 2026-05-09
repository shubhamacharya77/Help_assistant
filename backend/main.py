from fastapi import FastAPI,status,HTTPException
from router.user_query import router as user_router 
from router.docs_upload import router as doc_router
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.include_router(user_router)
app.include_router(doc_router)
@app.get("/",status_code=status.HTTP_200_OK)

async def healthCheck():
    try:
        return {"message": "Server is running...."}
    except HTTPException as e:
        return{"error":e}
