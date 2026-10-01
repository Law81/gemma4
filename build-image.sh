#!/usr/bin/env sh
set -eu

IMAGE_NAME="${IMAGE_NAME:-emploi}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
BUILD_CONTEXT="${BUILD_CONTEXT:-.}"
DOCKERFILE="${DOCKERFILE:-Dockerfile}"

echo "Construction de l'image Docker ${IMAGE_NAME}:${IMAGE_TAG}..."
docker build --pull --tag "${IMAGE_NAME}:${IMAGE_TAG}" --file "${DOCKERFILE}" "${BUILD_CONTEXT}"

echo "Image mise à jour : ${IMAGE_NAME}:${IMAGE_TAG}"