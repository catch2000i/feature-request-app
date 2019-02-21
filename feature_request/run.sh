docker build -f Dockerfile_feature_request -t basemachine_feature_request .
docker run -ti -p 5000:5000 basemachine_feature_request
