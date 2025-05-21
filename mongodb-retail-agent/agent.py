import os

import pymongo
import random

import certifi
import vertexai
from agents import Agent
from vertexai.language_models import TextEmbeddingModel


def generate_embeddings(query):
    vertexai.init(project="gcp-pov", location="us-central1")

    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([query])
    return embeddings[0].values


def product_details_search(query: str) -> str:
    """Query MongoDB and return queried results.

    Args:
      user query about amazon products: str

    Returns:
      results from MongoDB as a document.
    """
    client = pymongo.MongoClient(os.environ.get("CONNECTION_STRING"), tlsCAFile=certifi.where())
    vector_embeddings = generate_embeddings(query)
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'vector_index',
                'path': 'embeddings',
                'queryVector': vector_embeddings,
                'numCandidates': 50,
                'limit': 5
            }
        }]
    result = client["amazon"]["products-updated"].aggregate(pipeline)
    docs = []
    for i in result:
        docs.append(i["text"])
    return docs


def update_profile_data(user: str, interest: str) -> str:
    """Query MongoDB for the user name provided and update the document with interests if new interests is provided by the user.
      Args:
        user id from user input in form of Name : str
        interest as string : str

      Returns:
          success or failure message.
    """
    pass


def check_inventory(product: str) -> str:
    """Query MongoDB inventories with product name.
          Args:
            product name : str

          Returns:
              inventory details
    """
    from pymongo import MongoClient
    client = MongoClient(
        os.environ.get("CONNECTION_STRING"),
        tlsCAFile=certifi.where())
    db = client["amazon"]  # Replace with your database name
    collection = db["inventory"]  # Replace with your collection name
    document = collection.find_one({"product_name": product})  # No filter, returns the first document found
    print("inside Check Inventory")
    if document:
        del document["_id"]
        return document
    else:
        return "No document found."


def summarise_conversation(user: str) -> str:
    pass


def get_interests(user: str) -> str:
    """
    You are a customer service agent named Chatty. Always welcome user with positive chats. For customer queries
    related to their interest run this tool to query mongodb using user id and return the interest. This tool is
    trigger when the user mentions his name or his interests in product he wants to buy. Call the
    product_details_search tool once you have find the interests

      Args:
        user id from user input in form of Name : str

      Returns:
          results from MongoDB as a string.
    """
    from pymongo import MongoClient
    client = MongoClient(os.environ.get("CONNECTION_STRING"), tlsCAFile=certifi.where())
    db = client["amazon"]  # Replace with your database name
    collection = db["users"]  # Replace with your collection name
    document = collection.find_one({"first_name": user})  # No filter, returns the first document found
    print("inside interests")
    if document:
        return document["intrest"]
    else:
        return "No document found."


def get_faq(query: str) -> str:
    """
    If the queries are related to FAQ or any issues related to products, this tool is used to query the MongoDB Database and return the results.

    Args:
      user query about amazon products: str

    Returns:
      results from MongoDB as a document.
    """
    client = pymongo.MongoClient(os.environ.get("CONNECTION_STRING"), tlsCAFile=certifi.where())
    vector_embeddings = generate_embeddings(query)
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'vector_index',
                'path': 'embeddings',
                'queryVector': vector_embeddings,
                'numCandidates': 1,
                'limit': 1
            }
        }]
    result = client["amazon"]["products-faq"].aggregate(pipeline)
    for i in result:
        return i["text"]


root_agent = Agent(
    model='gemini-1.5-flash',
    name='data_processing_agent',
    instruction=""" 
    Start the Conversation with the user being a positive and friendly agent. Introduce yourself as 
    "eChatty" and ask user how can you help them today. You are a customer agent for an ecommerce company and you are 
    here to help the user with their shopping needs. 
    
    call get_interests only for below scenarios: 
    1. As soon as the user provids his name use the name as id to find 
    the user interests using the get_interests tool. 
    2. For any queries that has "interest" or "recommendation" or 
    "recommend" or realted terms call get_interests tool with user name as input.
    3. If the Name is provided call get_interests tool to get the user interests.
    If the name was not provided at the beginning and the user is asking to recommend something based on his 
    interests, ask the user for his name. If you find the name in the query Capitalize the first letter of the 
    Name while passing to get_interests tool. 
    
    call the product_details_search only for the below scenarios:
    1. As soon as you get the user intretsts from get_interests tool pass the user intrest as input to 
    product_details_search and query MongoDB Vector Search using product_details_search tool. 
    The product_details_search tool returns list of documents. Process the documents before replying back to the user. 
    2. For any queries related specific products like t-shirts, shoes etc. you must call the product_details_search tool 
    directly without calling get_interests tool irrespective of the Name field provided or not. 
    
    call the check_inventory only for the below scenarios:
    1. call check inventory only if the user explicitly asks to check for availability. or else redirect the query to 
    product_details_search tool.
    
    Additional instructions:
    1. Ask about the details only  if you don't understand the query and not able to search. 
    2. Always derive the Product name from returned message to check the inventory using check_inventory tool.  
    3. You can also use multiple tools in parallel by calling functions in parallel. 
    4. Do not search over internet and don't generate answers based on your own knowledge.  
    
    call summarise_conversation only for below scenario:
    1. Ask user if he has any question further once you recommend a product or return back his interests. If the user has 
    no further questions, summarize the conversation for the user and call the summarise_conversation tool. pass the user
    name and summary generated to the tool so that it can be saved. Reply the user with summary. 
    """ ,
    tools=[
        product_details_search,
        get_interests,
        get_faq,
        check_inventory
    ],
    flow='single',
)
