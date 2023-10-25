export PROJECT_ID=britemdb-402122
export BILLING_ACCOUNT_ID=melnaquib.gcp@gmail.com
export APP=britemdb
export PORT=8080
#export REGION="europe-north1"
export REGION="us-east1"
export TAG="gcr.io/$PROJECT_ID/$APP"
export IMAGE="$APP"
export TAG="0.2.0"
export REPOSITORY=britemdb
export IMAGE_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY"


#gcloud projects create $PROJECT_ID --name="My FastAPI App"
gcloud config set project $PROJECT_ID
#gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT_ID

# gcloud services enable

gcloud services enable \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  storage-component.googleapis.com \
  containerregistry.googleapis.com \
  firebase.googleapis.com \
  firestore.googleapis.com \


if gcloud artifacts repositories describe $REPOSITORY --location=$REGION > /dev/null 2>&1; then
    echo "Artifact Registry repository '$REPOSITORY' already exists."
else
    echo "Creating Artifact Registry repository '$REPOSITORY'..."
    gcloud artifacts repositories create $REPOSITORY --repository-format=docker --location=$REGION
fi

echo "DOCKER BUILD"
docker build -t $IMAGE:$TAG -t $IMAGE_PATH/$IMAGE:$TAG .
echo "DOCKER PUSH"
docker push $IMAGE_PATH/$IMAGE:$TAG


#gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE:$IMAGE_TAG" --ignore-file .gcloudignore
#gcloud builds submit --tag $TAG

echo "CLOUD RUN"
gcloud run deploy $APP --image $IMAGE_PATH/$IMAGE:$TAG --platform managed --region $REGION --allow-unauthenticated
gcloud run services describe $APP --region $REGION
URL=$(gcloud run services describe $APP --region $REGION --format 'value(status.url)')
echo "Service can be accessed at"
echo $URL

echo "to cleanup;"
echo gcloud run services delete $APP --region $REGION
# gcloud run services delete britemdb --region europe-north1
