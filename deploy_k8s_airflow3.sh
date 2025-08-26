
export IMAGE_NAME=spatial-dags
export IMAGE_TAG=0.0.1
export NAMESPACE=airflow
export RELEASE_NAME=airflow

docker build --pull --tag $IMAGE_NAME:$IMAGE_TAG -f Dockerfile . 
kind load docker-image $IMAGE_NAME:$IMAGE_TAG


helm upgrade $RELEASE_NAME apache-airflow/airflow \
    --namespace $NAMESPACE -f helm-chart/helm-values-airflow3.yaml \
    --set-string images.airflow.tag="$IMAGE_TAG" \
    --debug

kubectl port-forward svc/$RELEASE_NAME-api-server 8080:8080 --namespace $NAMESPACE