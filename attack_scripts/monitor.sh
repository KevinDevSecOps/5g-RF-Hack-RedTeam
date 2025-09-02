#!/bin/bash
echo "📊 Starting monitoring..."

check_services() {
    services=("5g-redteam-core" "postgres" "redis" "prometheus")
    for service in "${services[@]}"; do
        if docker ps | grep -q $service; then
            echo "✅ $service is running"
        else
            echo "❌ $service is down"
            return 1
        fi
    done
}

check_metrics() {
    echo "📈 Checking metrics..."
    curl -s http://localhost:9090/metrics | grep rf_ || echo "No RF metrics found"
}

check_health() {
    echo "❤️ Health check..."
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health)
    if [ "$response" -eq 200 ]; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed: $response"
    fi
}

check_services
check_health
check_metrics