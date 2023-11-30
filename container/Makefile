DOCKER_USERNAME=<Docker Hub username>
BASE_IMAGE = "debian:11"
IMAGE_NAME = "rdkit-df"
TAG = "latest"
REMOTE_IMAGE_NAME="$(DOCKER_USERNAME)/$(IMAGE_NAME)"

build:
	echo $(BASE_IMAGE)
	docker pull $(BASE_IMAGE)
	docker build -f Dockerfile -t "${IMAGE_NAME}:${TAG}" .

push:
	docker tag ${IMAGE_NAME}:${TAG} ${REMOTE_IMAGE_NAME}:${TAG}
	docker push "${REMOTE_IMAGE_NAME}:${TAG}"

run:
	docker run -ti --rm --entrypoint=/bin/bash -v `pwd`:/host ${IMAGE_NAME}

info:
	echo "REMOTE_IMAGE_NAME="$(REMOTE_IMAGE_NAME)
