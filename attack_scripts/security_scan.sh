#!/bin/bash
echo "🔒 Running security scan..."

# Scan for vulnerabilities
scan_dependencies() {
    echo "📦 Scanning Python dependencies..."
    pip-audit || echo "pip-audit not installed"
    
    echo "🦀 Scanning Rust dependencies..."
    cargo audit --version && cargo audit || echo "cargo audit not available"
}

scan_container() {
    echo "🐳 Scanning container..."
    docker scan 5g-redteam-core:latest || echo "Docker scan not available"
}

check_security() {
    echo "🔍 Checking security settings..."
    
    # Check running as non-root
    if [ "$(id -u)" -eq 0 ]; then
        echo "❌ Running as root!"
    else
        echo "✅ Running as non-root user"
    fi
    
    # Check capabilities
    echo "📋 Capabilities:"
    getpcaps 1
}

generate_report() {
    echo "📄 Generating security report..."
    echo "Security Scan Report - $(date)" > security-report.txt
    echo "=================================" >> security-report.txt
    whoami >> security-report.txt
    uname -a >> security-report.txt
}

scan_dependencies
scan_container
check_security
generate_report

echo "🔒 Security scan completed!"