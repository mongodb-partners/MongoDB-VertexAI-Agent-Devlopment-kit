# Configure and Deploy agent on Kubernetes
```
gcloud auth configure-docker us-docker.pkg.dev
docker build -t af_mongodb -f mongodb-retail-agent-Dockerfile .
docker run -e PROJECT=gcp-pov af_mongodb

docker tag af_mongodb gcr.io/iamtests-315719/af_mongodb:v0.1
docker push gcr.io/iamtests-315719/af_mongodb:v0.1



docker tag af_mongodb gcr.io/gcp-pov/af_mongodb:v0.1
docker push gcr.io/gcp-pov/af_mongodb:v0.1
```

### enable workload identity
```
gcloud container clusters update gke-psc-l4 \
     --workload-pool=iamtests-315719.svc.id.goog \
     --location=us-west2-a

gcloud iam service-accounts create afmongo \
     --project=iamtests-315719

gcloud projects add-iam-policy-binding iamtests-315719 \
    --member="serviceAccount:afmongo@iamtests-315719.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud iam service-accounts add-iam-policy-binding afmongo@iamtests-315719.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:iamtests-315719.svc.id.goog[default/afmongo]"

kubectl annotate serviceaccount afmongo \
    iam.gke.io/gcp-service-account=afmongo@iamtests-315719.iam.gserviceaccount.com \
    --namespace default
```
