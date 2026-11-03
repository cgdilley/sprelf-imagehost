
import os
import boto3
from pathlib import Path
from ruamel.yaml import YAML
import argparse
import string
import random
import botocore.client
import sys
import mimetypes

Y = YAML()
Y.default_flow_style = False
Y.indent(mapping=2, sequence=2, offset=2)

HOME = Path.home()
SETTINGS = HOME / ".sprelf" / "imghost" / "settings.yaml"


#


def main():
    args = sys.argv[1:]
    settings = {}
    if os.path.exists(SETTINGS):
        with open(SETTINGS, "r") as f:
            settings = Y.load(f)

    parser = argparse.ArgumentParser(description="Upload an image to host.")
    parser.add_argument("path", help="The path to the image to upload.")
    parser.add_argument("--custom", "-c", help="A custom string to set as the link", default=None)
    parser.add_argument("--permanent", "-P", help="Stores the image in S3 permanently.  Without this flag, "
                                                  "images will expire in 30 days.", action="store_true")
    parser.add_argument("--profile", help="The AWS profile to use", default=None)
    parser.add_argument("--domain", help="The domain to use for the link", default=None)
    parser.add_argument("--bucket", help="The bucket to upload to.", default=None)

    options = parser.parse_args(args)

    profile_name = options.profile or settings.get("aws_profile")
    bucket_name = options.bucket or settings.get("bucket_name")
    domain = options.domain or settings.get("domain")

    if not profile_name or not bucket_name or not domain:
        raise ValueError("Missing required settings: aws_profile, bucket_name, domain")

    s3 = boto3.Session(profile_name=profile_name).client('s3')

    image_type = mimetypes.guess_type(options.path)[0] or "application/octet-stream"

    if not options.custom:
        short = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        if not options.permanent:
            short = f"t{short}"
    else:
        short = options.custom
        if options.permanent and short.startswith("t"):
            short = f"p/{short}"

    try:
        s3.upload_file(Filename=options.path, Bucket=bucket_name, Key=short,
                       ExtraArgs={
                           "ContentType": image_type
                       })
        print(f"{domain}/{short}")
    except botocore.client.ClientError as e:
        print(f"Error: {e}")
