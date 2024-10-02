# Vertex AI Agent SDK for building RAG with MongoDB Atlas

### Requirements

1. [MongoDB Atlas Cluster](https://www.mongodb.com/docs/guides/atlas/cluster/) on [Google Cloud](https://www.mongodb.com/docs/atlas/reference/google-gcp/)
2. [Google Cloud console](https://console.cloud.google.com/welcome/new) access.
3. Vertex AI colab enterprise for Google cloud console.
4. The tools for agents uses vertexAI extensions. refer MongoDB [github](https://github.com/mongodb-partners/MongoDB-VertexAI-extensions) to set up the extensions. 


### Setup
Follow the instructions in the Python notebooks
 1. Log in to MongoDB Atlas console, On cluster navigation page click on 3 dots (...) and view all clusters. Click on 3 dots in front of your cluster name and Click on Load sample documents.
 2. Navigate to DataAPI and select DataAPI endpoint. Create an API key for the same from the DataAPI page by navigating to users.
    **Note**: DataAPI on MongoDB is being deprecated by September 2025, We will work on alternative solution for creating https endpoints and update the doc soon.
 4. extensions for MongoDB: To build MongoDB extension. Update the files as per instructions provided in the notebook
 5. Agent-SDK-use-case: To build and deploy app for Agent builder SDK

