from fastapi import APIRouter,status,HTTPException
from pydantic import BaseModel
from service.tools import web_search
from service.vectorDB import get_vectorstore 
from service.filter import FilterQuery
from service.prompts import Prompts
from service.models import Models
from langchain.agents import create_agent
router=APIRouter()
query_filter=FilterQuery()
model=Models()
prompts=Prompts()
class Query_schema(BaseModel):
    query:str
@router.post("/user_query",status_code=status.HTTP_200_OK)
async def user_query(request:Query_schema):
    try:

        #filter/structure response 
        filter_response=query_filter.filter_query(request.query)

        #final prompt  with relevant docs 
        final_prompt=prompts.final_response(filter_response)

        #agent createtion and final generation 
        agent=create_agent(
            model=model.chat_model(),
            tools=[web_search],
            system_prompt=final_prompt.to_string()
        )
        final_response=agent.invoke({"user_query":final_prompt})

        #store the generation 
        get_vectorstore().add_query(request.query)

        return {"response": final_response}

    except HTTPException as e:
        raise e