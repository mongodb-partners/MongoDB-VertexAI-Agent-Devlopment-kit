import pymongo
import random

import vertexai
from agents import Agent
from vertexai.language_models import TextEmbeddingModel


def generate_embeddings(query):
    vertexai.init(project="gcp-pov", location="us-central1")

    model = TextEmbeddingModel.from_pretrained("text-embedding-004	")
    embeddings = model.get_embeddings([query])
    return embeddings[0].values


def product_details_search(query: str) -> str:
    """Query MongoDB and return queried results.

    Args:
      user query about amazon products: str

    Returns:
      results from MongoDB as a document.
    """
    client = pymongo.MongoClient("MongoDB connection string")
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
    result = client["amazon"]["products-updated"].aggregate(pipeline)
    print(">>>>>>>>>>>>>>>>")
    for i in result:
        return i["text"]


def get_intrests(user: str) -> str:
    """
      You are a customer service agent named Chatty. Always welcome user with positive chats.
      For customer queries related to their intrest run this tool to query mongodb using user id and return the intrest.
      This tool is trigger when the user mentions his name or his intrests in product he wants to buy.

      Args:
        user id from user input in form of Name : str

      Returns:
          results from MongoDB as a string.
    """
    from pymongo import MongoClient
    client = MongoClient("mongodb connection string")
    db = client["amazon"]  # Replace with your database name
    collection = db["users"]  # Replace with your collection name
    document = collection.find_one({"first_name": user})  # No filter, returns the first document found
    print(">>>>>>>>>>>>>>>>>>>")
    print("inside intrests")
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
    client = pymongo.MongoClient("mongodb+srv://venkatesh:ashwin123@freetier.kxcgwh2.mongodb.net")
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
      Start the Conversation with the user being a positive and friendly agent. Introduce yourself as "eChatty" and ask user how can you help them today.
      You are a customer agent for an ecommerce company and you are here to help the user with their shopping needs. You use the MongoDB Database to search for products, you use product_details_search to query the user query.
      You answer questions about products, help users find products, and provide information about products from the MongoDB Database using Vector Search.
      When you are asked about anything related to products, ask product name or description. you must call the product_details_search tool with user input in string format.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      do not search over internet and don't generate answers based on your own knowledge.
      You can ask the agent to query about user intrests using get_intrests tool. return the intrests of the user based on the user id. In this senario the user id is the users name.
      If the user queries for intrests, reply the user with the intrests of the user using the get_intrests tool and than use the product_details_search tool to query the user query.
      If the user queries for FAQ or if the user query does not match any of the above tool reply the user query by running the get_faq tool. All the issues of the users that has sad tone should end up here. 
      If you are not able to resolve user issue with FAQ ask the user if he wants to connect to the customer agent for further help.
    """,
    tools=[
        product_details_search,
        get_intrests,
        get_faq
    ],
    flow='single',
)
