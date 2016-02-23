#!/bin/bash

BACKUP_PATH='/backup'
CBBACKUP_PATH='/opt/couchbase/bin/'

timestamp=$(date +"%Y-%m-%d")
buckets=$(couchbase-cli bucket-list -c ${CB_HOST}:8091 -u ${CB_ADMIN_USER} -p ${CB_ADMIN_PASS} | grep -v ':')
buckets=($buckets)

aws configure set aws_access_key_id ${AWS_ACCESS_KEY}
aws configure set aws_secret_access_key ${AWS_SECRET_KEY}
aws configure set default.region ${AWS_REGION}

for bucket in "${buckets[@]}"
do
	echo "--- Backing up $bucket ---"
	/opt/couchbase/bin/cbbackup http://${CB_HOST}:8091 $BACKUP_PATH/$bucket \
		--username=$CB_ADMIN_USER --password=$CB_ADMIN_PASS \
		--bucket-source=$bucket \

	tar -czvf $BACKUP_PATH/$bucket.tar.gz $BACKUP_PATH/$bucket

	echo "--- Uploading $bucket ---"
	aws s3 cp $BACKUP_PATH/$bucket.tar.gz s3://${AWS_BACKUP_BUCKET}/$timestamp/ \
		--storage-class STANDARD_IA
	rm -f $BACKUP_PATH/$bucket.tar.gz
done