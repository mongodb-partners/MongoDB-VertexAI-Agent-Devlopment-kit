# Conversational Commerce: Transforming Customer Experience with Vertex AI and MongoDB Atlas
**Author**: MongoDB(https://accounts.mongodb.com).
**NOTE**: This repo is in progress. More features for reatil agents will be added soon.


Transform customer interactions with conversational agents built using the Google Vertex AI Agent Development Kit, powered by MongoDB Atlas. Leverage vector search and query language within Atlas to provide personalized, context-aware assistance, enhancing the shopping journey and driving sales. This solution addresses impersonal e-commerce support by automating tasks, improving efficiency, and delivering data-driven insights, ultimately boosting conversions and customer satisfaction.

### Setup MongoDB Atlas
1. The first step is to create a [MongoDB Atlas cluster on Google Cloud](https://www.mongodb.com/products/platform/atlas-cloud-providers/google-cloud). 
2. Configure IP [access list entries](https://www.mongodb.com/docs/atlas/security/ip-access-list/) and a [database user](https://www.mongodb.com/docs/atlas/security-add-mongodb-users/) for accessing the cluster using the connection string.
3. Get the [connection string](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/) for MongoDB.

Update the connection string in your before running agent framework by exporting it as CONNECTION_STRING (done in upcoming steps).  

### Install requirements
```
pip3 install google_genai_agents-0.0.2.dev20250204+723246417-py3-none-any.whl
pip3 install -r requirements.txt
```

### Before you run the Agents
1. Download the data files from [data](mongodb-retail-agent/data) folder. 
2. Upload the data to MongoDB Atlas using the load_data scipt under mongodb-retail-agent/data folder using following command.
``` python3 mongodb-retail-agent/data/load_data.py ```
3. This will create the 2 collections "products" and "users" in MongoDB that already has embedding generated on the products data.
4. Navigate to MongoDB Atlas and Create a [vector index](https://www.mongodb.com/docs/compass/current/indexes/create-vector-search-index/) on text field. use below snippet to create index on products data using JSON editor on MongoDB Atlas search page.
   ```
   {
    "fields": [
    {
        "numDimensions": 768,
        "path": "embeddings",
        "similarity": "cosine",
        "type": "vector"
        }
    ]
    }
    ```

### Run agent framework
To build an agent, you create a folder for that agent, named after the agent and contains at least the following files:
- **agent.py**: The main file for the agent. You have to define your root agent under the global variable root_agent.
- **__init__.py**: The python module file. It has to at least contain a line from agents import Agent to import the Agent class.

```
export GOOGLE_GENAI_USE_VERTEXAI=1
export GOOGLE_CLOUD_PROJECT=<Your project Name>
export GOOGLE_CLOUD_LOCATION=us-central1
export CONNECTION_STRING="<Your connection string>"

af web .
```
