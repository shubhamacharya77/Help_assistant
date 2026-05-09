from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from pydantic import Field 
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from service.vectorDB import get_vectorstore

class SupportResponse(BaseModel):
    user_query: str = Field(description="Original query")
    cleaned_query: str = Field(description="Refined query")
    issue_type: str = Field(description="payment/order_status/product_issue/etc")
    priority: str = Field(description="low/medium/high")
    sentiment: str = Field(description="positive/neutral/negative")

parser = PydanticOutputParser(pydantic_object=SupportResponse)



class Prompts():
    def __init__(self):
        pass
    def Query_structure(self,user_query):
        prompt=ChatPromptTemplate.from_template(
            template="""
                You are an AI assistant designed to analyze customer support queries and extract structured information.

                Your task is to:

                Understand the user's query.
                Identify the core issue.
                Classify the issue into a predefined category.
                Return ONLY valid JSON.
                Do NOT include explanation, markdown, or extra text.

                Format_instructions-
                {format_instructions}

                User query
                {user_query}""" )
        
        filter_prompt=prompt.invoke({"user_query":user_query,"format_instructions":parser.get_format_instructions()})
        return filter_prompt
    
    def final_response(self,structure_response):
        relevant_docs=get_vectorstore().query_search(structure_response)
        prompt=PromptTemplate(
            template="""
You are a professional and polite customer support assistant.

You will receive a JSON input containing:
- user_query
- cleaned_query
- issue_type
- priority
- sentiment

and relevant old tickets,documents
Your task is to generate a helpful, polite, and concise response to the user based on this structured data.

Rules (STRICT):
1. Always respond politely and professionally.
2. Use the query to understand the core issue.
3. Adapt tone slightly based on "sentiment":
   - negative → empathetic and reassuring
   - neutral → clear and helpful
   - positive → appreciative and friendly
4. Consider "issue_type" to tailor the response (e.g., payment, order_status, product_issue).
5. If "priority" is high → acknowledge urgency and assure quick resolution.
6. Do NOT mention the JSON, fields, or internal processing.
7. Do NOT repeat the exact query unless necessary.
8. Keep the response clear and to the point (avoid long explanations).
9. dont use you're knowledge base either use relevant docs or search tool (strict).
10.Never generate harmful, rude, or speculative content.
11.don't send tool call request in content section.
12.if there is any need of tool call then use agent and call the tool

Input JSON:
{input_json}

Relevant source/docs:
{relevant_docs}


Output:
- Only return the final response message to the user (no JSON, no explanation).
""",input_variables=["input_json","relevant_docs"]
        )
        final_prompt=prompt.invoke({
            "input_json":structure_response,
            "relevant_docs":relevant_docs
        })
        return final_prompt




