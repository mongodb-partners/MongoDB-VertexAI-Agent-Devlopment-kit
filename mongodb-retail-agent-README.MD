### gcloud auth configure-docker us-docker.pkg.dev
### docker build -t af_mongodb -f mongodb-retail-agent-Dockerfile .
### docker run -e PROJECT=<project name> af_mongodb


### docker tag af_mongodb gcr.io/<project_name>/af_mongodb:v0.1
### docker push gcr.io/<project_name>/af_mongodb:v0.1


### enable workload identity
### gcloud container clusters create gke-psc-l4 --workload-pool=<project_name>.svc.id.goog --location=us-west2-a

### gcloud iam service-accounts create afmongo --project=<project_name>

### gcloud projects add-iam-policy-binding <project_name> --member="serviceAccount:afmongo@<project_name>.iam.gserviceaccount.com" --role="roles/aiplatform.user"

### gcloud iam service-accounts add-iam-policy-binding afmongo@<project_name>.iam.gserviceaccount.com --role roles/iam.workloadIdentityUser --member "serviceAccount:<project_name>.svc.id.goog[default/afmongo]"
### kubectl annotate serviceaccount afmongo iam.gke.io/gcp-service-account=afmongo@<project_name>.iam.gserviceaccount.com --namespace default

### kubectl apply -f mongodb-retail-agent/k8s.yaml
