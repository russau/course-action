#!/usr/bin/env python3
import yaml
import boto3
import os

source_bucket="russ-courses-source"
destination_bucket="russ-courses-built"
s3 = boto3.client('s3')
workspace = os.getenv('GITHUB_WORKSPACE', default="/app")

# open and read manifest yaml file
try:
    with open(f'{workspace}/manifest.yaml', 'r') as file:
        manifest = yaml.safe_load(file)
        print("Manifest file loaded successfully.")
except FileNotFoundError:
    print("Manifest file not found.")
    exit(0)

COURSE_CODE = manifest['course_code']

for language in manifest['languages']:
    language_code = language['code']
    print(f"Downloading {language_code} files")
    prefix = f"{COURSE_CODE}/{language_code}/"
    temp_dir = f"/tmp/{prefix}"
    version = language['version']

    # make a tmp directory for each language
    os.makedirs(temp_dir, exist_ok=True)

    # download all the objects with a prefix from an s3 bucket into a tmp
    for obj in s3.list_objects(Bucket=source_bucket, Prefix=prefix)['Contents']:
        print(f" Downloading {obj['Key']}")
        s3.download_file(source_bucket, obj['Key'], f"/tmp/{obj['Key']}")

    # create a zip file of each directory
    zipname = f"{COURSE_CODE}_{version}_{language_code}.zip"
    print(f" Creating zip file {zipname}")
    os.system(f"cd {temp_dir} && zip -r /tmp/{zipname}.zip . > /dev/null")
    print(f" Uploading {zipname} to {destination_bucket}")
    s3.upload_file(f"/tmp/{zipname}.zip", destination_bucket, zipname)
    print()
