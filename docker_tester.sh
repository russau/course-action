#!/bin/bash
AK=$(aws configure get aws_access_key_id --profile personal)
SAK=$(aws configure get aws_secret_access_key --profile personal)
docker run -it --rm -e AWS_ACCESS_KEY_ID=$AK \
-e AWS_SECRET_ACCESS_KEY=$SAK \
-e AWS_DEFAULT_REGION=us-west-2 \
-v $(pwd)/sample_manifest.yaml:/app/manifest.yaml \
action-test:latest
