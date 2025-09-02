#!/bin/bash
set -e

echo "💾 Starting backup process..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/$TIMESTAMP"
LOG_FILE="/var/log/backup_$TIMESTAMP.log"

# Load configuration
CONFIG_FILE="deployments/backup/config/backup_config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    DB_HOST=$(yq e '.database.host' $CONFIG_FILE)
    DB_NAME=$(yq e '.database.name' $CONFIG_FILE)
    DB_USER=$(yq e '.database.user' $CONFIG_FILE)
    RETENTION_DAYS=$(yq e '.retention.days' $CONFIG_FILE)
else
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

mkdir -p $BACKUP_DIR
exec > >(tee -a $LOG_FILE) 2>&1

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

backup_database() {
    log "Backing up PostgreSQL database..."
    export PGPASSWORD=$(yq e '.database.password' $CONFIG_FILE)
    pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -F c -b -v -f "$BACKUP_DIR/database.backup"
    
    if [ $? -eq 0 ]; then
        log "✅ Database backup completed"
    else
        log "❌ Database backup failed"
        exit 1
    fi
}

backup_redis() {
    log "Backing up Redis..."
    redis-cli SAVE
    cp /var/lib/redis/dump.rdb "$BACKUP_DIR/redis.rdb"
    log "✅ Redis backup completed"
}

backup_configs() {
    log "Backing up configurations..."
    tar -czf "$BACKUP_DIR/configs.tar.gz" \
        config/ \
        deployments/ \
        scripts/ \
        --exclude="*.log" \
        --exclude="*.tmp"
    log "✅ Configurations backup completed"
}

backup_data() {
    log "Backing up application data..."
    tar -czf "$BACKUP_DIR/data.tar.gz" \
        data/ \
        logs/ \
        --exclude="*.tmp" \
        --exclude="cache/*"
    log "✅ Application data backup completed"
}

encrypt_backup() {
    log "Encrypting backup..."
    GPG_RECIPIENT=$(yq e '.encryption.gpg_recipient' $CONFIG_FILE)
    if [ -n "$GPG_RECIPIENT" ]; then
        gpg --encrypt --recipient "$GPG_RECIPIENT" "$BACKUP_DIR/database.backup"
        gpg --encrypt --recipient "$GPG_RECIPIENT" "$BACKUP_DIR/configs.tar.gz"
        gpg --encrypt --recipient "$GPG_RECIPIENT" "$BACKUP_DIR/data.tar.gz"
        log "✅ Backup encryption completed"
    fi
}

upload_to_cloud() {
    log "Uploading to cloud storage..."
    CLOUD_TYPE=$(yq e '.cloud.type' $CONFIG_FILE)
    
    case $CLOUD_TYPE in
        "aws")
            aws s3 sync "$BACKUP_DIR" "s3://$(yq e '.cloud.aws.bucket' $CONFIG_FILE)/$TIMESTAMP/"
            ;;
        "gcp")
            gsutil -m rsync -r "$BACKUP_DIR" "gs://$(yq e '.cloud.gcp.bucket' $CONFIG_FILE)/$TIMESTAMP/"
            ;;
        "azure")
            az storage blob upload-batch -d "$(yq e '.cloud.azure.container' $CONFIG_FILE)" -s "$BACKUP_DIR"
            ;;
        *)
            log "⚠️  No cloud storage configured"
            ;;
    esac
    log "✅ Cloud upload completed"
}

cleanup_old_backups() {
    log "Cleaning up old backups..."
    find /backup -type d -name "2*" -mtime +$RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null || true
    log "✅ Old backups cleanup completed"
}

generate_report() {
    log "Generating backup report..."
    TOTAL_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
    BACKUP_COUNT=$(find $BACKUP_DIR -type f | wc -l)
    
    cat > "$BACKUP_DIR/backup_report.json" << EOF
{
    "timestamp": "$TIMESTAMP",
    "status": "success",
    "backup_size": "$TOTAL_SIZE",
    "file_count": $BACKUP_COUNT,
    "components": [
        "database",
        "redis",
        "configurations",
        "application_data"
    ],
    "encryption": "$([ -n "$GPG_RECIPIENT" ] && echo "enabled" || echo "disabled")",
    "cloud_upload": "$CLOUD_TYPE"
}
EOF
    log "✅ Backup report generated"
}

# Main execution
main() {
    log "Starting backup process $TIMESTAMP"
    
    backup_database
    backup_redis
    backup_configs
    backup_data
    encrypt_backup
    upload_to_cloud
    cleanup_old_backups
    generate_report
    
    log "🎉 Backup process completed successfully!"
    exit 0
}

# Error handling
trap 'log "❌ Backup failed with error: $?"; exit 1' ERR
trap 'log "🛑 Backup interrupted"; exit 2' INT TERM

main