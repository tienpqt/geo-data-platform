
#Create k8s cluster 
kind delete cluster --name kind
kind create cluster --image kindest/node:v1.29.4 


# Use Helm to install Airflow docker image 3.0.2 python 3.11
helm repo add apache-airflow https://airflow.apache.org
helm repo update 

export IMAGE_NAME=spatial-dags
export IMAGE_TAG=0.0.1
export NAMESPACE=airflow
export RELEASE_NAME=airflow

docker build --pull --tag $IMAGE_NAME:$IMAGE_TAG -f Dockerfile . 
kind load docker-image $IMAGE_NAME:$IMAGE_TAG

kubectl create namespace $NAMESPACE
kubectl apply -f k8s/secrets/git-secrets.yaml

helm install $RELEASE_NAME apache-airflow/airflow \
    --namespace $NAMESPACE -f helm-chart/helm-values-airflow3.yaml \
    --set-string images.airflow.tag="$IMAGE_TAG" \
    --debug

kubectl port-forward svc/$RELEASE_NAME-api-server 8080:8080 --namespace $NAMESPACE