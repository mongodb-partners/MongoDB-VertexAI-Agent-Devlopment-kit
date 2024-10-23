# Vertex AI Agent SDK for building Agentic RAG with MongoDB Atlas

### Requirements

1. [MongoDB Atlas Cluster](https://www.mongodb.com/docs/guides/atlas/cluster/) on [Google Cloud](https://www.mongodb.com/docs/atlas/reference/google-gcp/)
2. [Google Cloud console](https://console.cloud.google.com/welcome/new) access.
3. Google Cloud Storage bucket.
4. Vertex AI colab enterprise for Google cloud console.
5. The tools for agents uses vertexAI extensions. refer MongoDB [github](https://github.com/mongodb-partners/MongoDB-VertexAI-extensions) to set up the extensions. 


### Setup
1. Setup the [api connection](./api_setup/README.md) to MongoDb Atlas.
2. Log in to MongoDB Atlas console, On cluster navigation page and naviage to Databases. click on 3 dots (...) and view all clusters. Click on 3 dots in front of your cluster name and Click on Load sample documents.
3. extensions for MongoDB: To build MongoDB extension run the notebook '_[1.extensions-for-mongodb-using-cloud-function.ipynb](./1.extensions-for-mongodb-using-cloud-function.ipynb)_'.
4. To test a sample use case on MongoDB Atlas, follow the instructions in notebook '[_2.agent-sdk-using-mongodb-extensions.ipynb_](./2.agent-sdk-using-mongodb-extensions.ipynb)'.



