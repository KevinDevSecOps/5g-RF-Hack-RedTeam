#!/bin/bash
set -e

echo "🚀 Deploying 5G RedTeam System..."

# Variables
ENV=${1:-production}
IMAGE_TAG="5g-redteam-core:latest"

build_image() {
    echo "📦 Building Docker image..."
    docker build -f deployments/docker/security/Dockerfile.security -t $IMAGE_TAG .
}

deploy_docker() {
    echo "🐳 Deploying with Docker Compose..."
    docker-compose -f deployments/docker/compose/docker-compose.$ENV.yml down
    docker-compose -f deployments/docker/compose/docker-compose.$ENV.yml up -d --build
}

deploy_kubernetes() {
    echo "☸️ Deploying to Kubernetes..."
    kubectl apply -f deployments/kubernetes/manifests/namespace.yaml
    kubectl apply -f deployments/kubernetes/manifests/
    kubectl rollout status deployment/5g-redteam-core -n redteam
}

monitor_deployment() {
    echo "📊 Monitoring deployment..."
    sleep 10
    curl -f http://localhost:5000/api/health || exit 1
    echo "✅ Deployment successful!"
}

case "$ENV" in
    production)
        build_image
        deploy_docker
        ;;
    kubernetes)
        deploy_kubernetes
        ;;
    *)
        echo "Usage: $0 {production|kubernetes}"
        exit 1
        ;;
esac

monitor_deployment