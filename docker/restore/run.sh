#!/bin/bash

CBRESTORE_PATH='/opt/couchbase/bin/'

aws configure set aws_access_key_id ${AWS_ACCESS_KEY}
aws configure set aws_secret_access_key ${AWS_SECRET_KEY}
aws configure set default.region ${AWS_REGION}

MOST_RECENT_FOLDER=$(aws s3 ls s3://leaguebot-backup | sort -r | head -1 | awk '{print $2}')
MOST_RECENT_BACKUP=$(aws s3 ls s3://leaguebot-backup/$MOST_RECENT_FOLDER | sort -r | head -1 | awk '{print $4}')
aws s3 cp s3://leaguebot-backup/$MOST_RECENT_FOLDER$MOST_RECENT_BACKUP /
tar -zxf /$MOST_RECENT_BACKUP 
rm -rf /$MOST_RECENT_BACKUP

$CBRESTORE_PATH/cbrestore /${MATCH_HISTORY_BUCKET} http://${CB_HOST}:8091 \
	--username=$CB_ADMIN_USER --password=$CB_ADMIN_PASS \
	--bucket-source=${MATCH_HISTORY_BUCKET} 
rm -rf /${MATCH_HISTORY_BUCKET}
