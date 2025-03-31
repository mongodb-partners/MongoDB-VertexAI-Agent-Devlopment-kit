import json
import os
import csv

import certifi
from pymongo import MongoClient

def load_csv_to_mongodb(csv_file_path, collection):
    """
    Loads data from a CSV file into a MongoDB Atlas collection.

    Args:
        csv_file_path (str): Path to the CSV file.
        connection_string (str): MongoDB Atlas connection string.
        database_name (str): Name of the MongoDB database.
        collection_name (str): Name of the MongoDB collection.
    """
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(os.environ.get("CONNECTION_STRING"),  tlsCAFile=certifi.where())
        db = client["amazon"]
        collection = db[collection]

        # Load CSV data
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Read CSV as a list of dictionaries

            data = list(reader) #convert the reader object to a list so it can be inserted.

        # Insert data into the collection
        if data:
            collection.insert_many(data)
            print(f"Successfully inserted {len(data)} ")
        else:
            print(f"CSV file is empty.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except csv.Error as e:
        print(f"Error: CSV parsing error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()

# Example usage (replace with your actual values)
products_json_file_path = "./mongodb-retail-agent/data/amazon.products-updated.csv"  # Replace with your JSON file path.
users_json_file_path = "./mongodb-retail-agent/data/amazon.users.csv"


load_csv_to_mongodb(products_json_file_path, "products")
load_csv_to_mongodb(users_json_file_path,"users")
