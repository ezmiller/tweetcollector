#!/bin/bash

mkdir ~/.aws

cat > ~/.aws/config <<EOL
[default]
region = us-east-1
EOL

AWS_ACCESS_KEY_ID=$(head -n 1 /run/secrets/aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(head -n 1 /run/secrets/aws_secret_access_key)

cat > ~/.aws/credentials <<EOL
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOL
