from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
)
from constructs import Construct


class CrossAccountS3ReadStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, environment: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.s3_bucket = s3.Bucket(
            self,
            "S3BucketSource",
            bucket_name=environment["S3_BUCKET_NAME"],
            event_bridge_enabled=environment["EVENTBRIDGE_ENABLED"],
            versioned=environment["VERSION_ENABLED"],
            removal_policy=RemovalPolicy.DESTROY,
            # auto_delete_objects=True,
        )

        for vendor_dict in environment["VENDORS"]:
            self.s3_bucket.add_to_resource_policy(
                iam.PolicyStatement(
                    sid=f"S3ListFolderFor{vendor_dict['VENDOR_NAME']}",
                    actions=["s3:ListBucket"],
                    principals=[iam.ArnPrincipal(vendor_dict["VENDOR_IAM_ROLE"])],
                    conditions={
                        "StringEquals": {
                            "s3:prefix": ["", vendor_dict["VENDOR_FOLDER"] + "/"]
                        }
                    },
                    resources=[self.s3_bucket.bucket_arn],
                )
            )
            self.s3_bucket.add_to_resource_policy(
                iam.PolicyStatement(
                    sid=f"S3GetFolderFor{vendor_dict['VENDOR_NAME']}",
                    actions=["s3:GetObject"],
                    principals=[iam.ArnPrincipal(vendor_dict["VENDOR_IAM_ROLE"])],
                    resources=[
                        f"{self.s3_bucket.bucket_arn}/{vendor_dict['VENDOR_FOLDER']}/*"
                    ],
                )
            )
