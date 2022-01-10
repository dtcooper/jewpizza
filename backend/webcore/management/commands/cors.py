import json

import boto3
from botocore.exceptions import ClientError

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-g", "--get", action="store_true", help="Get CORS for bucket")
        group.add_argument("-s", "--set", action="store_true", help="Set CORS for bucket")
        group.add_argument("-a", "--set-all", action="store_true", help="Set for all domains (*)")
        parser.add_argument(
            "domains",
            nargs="*",
            help="Domains to set for (default: {settings.DOMAIN_NAME})",
            default=[settings.DOMAIN_NAME],
        )

    def handle(self, *args, **options):
        session = boto3.session.Session()
        client = session.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        if options["set"] or options["set_all"]:
            if options["set"]:
                domains = options["domains"]
            else:
                domains = ["*"]

            cors_configuration = {
                "CORSRules": [
                    {
                        "AllowedHeaders": domains,
                        "AllowedMethods": ["GET", "PUT", "DELETE", "HEAD", "POST"],
                        "AllowedOrigins": ["*"],
                        "ExposeHeaders": ["ETag"],
                        "MaxAgeSeconds": 3000,
                    }
                ]
            }

            client.put_bucket_cors(Bucket=settings.AWS_STORAGE_BUCKET_NAME, CORSConfiguration=cors_configuration)

        try:
            response = client.get_bucket_cors(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchCORSConfiguration":
                raise CommandError(f"No CORS configuration for {settings.AWS_STORAGE_BUCKET_NAME}")
            else:
                raise e

        print(json.dumps(response["CORSRules"], indent=2, sort_keys=True))
