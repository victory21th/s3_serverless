<!--
title: 'S3 Handler'
description: 'This lambda function retrived newly created files in s3 bucket and print the content and move them to another directory.'
layout: Doc
framework: v1
platform: AWS
language: Python
authorLink: 'https://github.com/victory21th'
authorName: 'Rennan'
-->
# S3 File Handler

This lambda function retrived newly created files in s3 bucket and print the content and move them to another directory.
## Pre-requirement

You need to setup aws account and configure with **aws configure** command.
## Setup

```bash
npm install -g serverless
npm install
```
## Configuration
You can set configuration in serverless.yml
```bash

provider:
  name: aws
  runtime: python3.7

  stage: dev
  region: us-east-1
  environment:          <<<<<<<<<< **HERE**
        **S3_BUCKET_NAME**: rennantest123
        **S3_KEY_BASE**: Incoming
        **S3_NEW_KEY_BASE**: Processed

```

## Deploy

In order to deploy the endpoint simply run

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Generated requirements from /home/dev/work/Python/serverless_s3/requirements.txt in /home/dev/work/Python/serverless_s3/.serverless/requirements.txt...
Serverless: Using static cache of requirements found at /home/dev/.cache/serverless-python-requirements/bcfa0354bc5cbc23bd3ba35af4d4533e89dba1a465b20f4ce47a9413d818e5b3_slspyc ...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
.....
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service serverless-s3.zip file to S3 (9.09 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
.....................
Serverless: Stack update finished...
Service Information
service: serverless-s3
stage: dev
region: us-east-1
stack: serverless-s3-dev
resources: 7
api keys:
  None
endpoints:
  None
functions:
  main: s3_upload_handler
layers:
  None


```
## Test
Add a file in **Incoming** directory of the S3 bucket and then refresh the screen.

You will notice it has been moved to **Processed** directory and the content is printed in the **Cloudwatch**
