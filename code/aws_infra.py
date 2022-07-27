import json

import pulumi_aws as aws
from pulumi import AssetArchive, FileArchive, FileAsset, ResourceOptions
from pulumi import export as key_export

# 1. Copy GCS bucket to S3 (export.csv; 2.6kb for the hail example).
# The issue is Athena isn't in free tier, so we're blending the "labs" to make one lab on multiple clouds.
data_bucket = aws.s3.Bucket("laura-data-bucket")

data_object = aws.s3.BucketObject(
    "laura-csv",
    bucket=data_bucket.id,
    source=FileAsset("./extract.csv"),
    content_type="text/csv",
    opts=ResourceOptions(parent=data_bucket)
)

# 2. Run a Lambda that does the same pandas/matplotlib calcuations and serves via a function URL
lambda_policy_document = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            actions=["sts:AssumeRole"],
            principals=[
                aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="Service",
                    identifiers=["lambda.amazonaws.com"]
                )
            ],
            effect="Allow",
            sid=""
        )
    ]
)

iam_for_lambda = aws.iam.Role(
    "laura-iam-for-lambda",
    assume_role_policy=lambda_policy_document.json
)

# Create the role for the Lambda to assume
lambda_role = aws.iam.Role(
    "lambdaRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com",
            },
            "Effect": "Allow",
            "Sid": "",
        }]
    })
)

role_policy_attachment = aws.iam.RolePolicyAttachment(
    "lambdaRoleAttachment",
    role=lambda_role.id,
    policy_arn=aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE
)
role_policy_attachment_2 = aws.iam.RolePolicyAttachment(
    "laura-rpa-2",
    role=lambda_role.id,
    policy_arn=aws.iam.ManagedPolicy.AMAZON_S3_FULL_ACCESS
)

# TODO: Write up workshop with skeleton code to fill in for people.
# TODO: Update data to run something different.
# TODO: Bonus content: Simulation of a hurricane or something with scipy on GCP as a final demo
# TODO: Talk about bouncing around stacks, the limits of AWS free tier, etc.

s3fs_layer = aws.lambda_.LayerVersion(
    "laura-s3fs-lambda-layer",
    compatible_runtimes=["python3.9"],
    code=FileArchive("./layers/s3fs.zip"),  # NOTE: This file has to be a certain size.
    layer_name="kcdc-dev-compressed"
)

fsspec_layer = aws.lambda_.LayerVersion(
    "laura-fsspec-lambda-layer",
    compatible_runtimes=["python3.9"],
    code=FileArchive("./layers/fsspec.zip"),  # NOTE: This file has to be a certain size.
    layer_name="kcdc-dev-compressed-2"
)

function = aws.lambda_.Function(
    "laura-function",
    description="To analyze data for KCDC",
    runtime="python3.9",
    role=lambda_role.arn,
    handler="aws_main.lambda_handler",
    code=AssetArchive({
        ".": FileArchive("app")
    }),
    layers=[
        s3fs_layer.arn,
        fsspec_layer.arn,
        "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pandas:6",
        "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-matplotlib:1"
    ],
    timeout=120,
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            'BUCKET': data_bucket.id.apply(lambda i: f"{i}"),
            'DATA': data_bucket.bucket_domain_name.apply(lambda url: f"s3://{url}/laura-csv"),
            'BUCKET_NAME': data_bucket.bucket.apply(lambda n: f"{n}")
        }
    )
)

function_url = aws.lambda_.FunctionUrl(
    "laura-function-url",
    function_name=function.arn,
    authorization_type="NONE"
)

key_export("function-url", function_url.function_url)
