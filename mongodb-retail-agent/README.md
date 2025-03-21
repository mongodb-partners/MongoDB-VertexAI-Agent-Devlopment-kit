# Agent Framework - Retail use case for product recommandation

### Setup MongoDB Atlas

### Install requirements
```
pip3 install google_genai_agents-0.0.2.dev20250204+723246417-py3-none-any.whl
pip3 install -r requirements.txt
```

### Run agent framework
```
export GOOGLE_GENAI_USE_VERTEXAI=1
export GOOGLE_CLOUD_PROJECT=gcp-pov
export GOOGLE_CLOUD_LOCATION=us-central1

af web .
```
