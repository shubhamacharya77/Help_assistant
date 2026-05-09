from langchain_community.tools import  tool
import os 
from dotenv import load_dotenv
load_dotenv()
from serpapi import GoogleSearch

@tool
def web_search(user_query):
    """ this tool help get external data from web-search...."""
    try:
        params = {
        "api_key":os.getenv("GOOGLE_API_KEY_serpapi"),
        "engine":"google",
        "q": user_query
        }
        engine=GoogleSearch(params)
        response=engine.get_dict()
        if  response["ai_overview"]["text_blocks"] ==None:
            return response
        else:
            response
    except Exception as e:
        raise Exception(f"error :",e)

