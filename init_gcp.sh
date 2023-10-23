# gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com storage-component.googleapis.com containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com

if gcloud artifacts repositories describe $REPOSITORY_NAME --location=$REGION > /dev/null 2>&1; then
    echo "Artifact Registry repository '$REPOSITORY_NAME' already exists."
else
    echo "Creating Artifact Registry repository '$REPOSITORY_NAME'..."
    gcloud artifacts repositories create $REPOSITORY_NAME --repository-format=docker --location=$REGION
fi

# Build image to artifact registry
gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME:$IMAGE_TAG" --ignore-file .gcloudignore


# docker push us-central1-docker.pkg.dev/someproject-123/docker-repo/fast-api:1.0
