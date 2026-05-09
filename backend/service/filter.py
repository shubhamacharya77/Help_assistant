from pydantic import BaseModel
from service.models import Models
from service.prompts import Prompts
from dotenv import load_dotenv
import os 
prompts=Prompts()
model=Models()
load_dotenv()
class user_query(BaseModel):
    query:str
class FilterQuery():
    def __init__(self):
        pass 
    def filter_query(self,user_query):
        filter_prompt=prompts.Query_structure(user_query)
        filter_response=model.chat_model().invoke(filter_prompt)
        return filter_response.content
    
