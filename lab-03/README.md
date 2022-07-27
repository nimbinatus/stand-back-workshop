# Lab 3: Cloud Hopping

At the beginning of this workshop, we talked about being able to hop from one cloud to another to do just a bit more personal scientific analysis, such as if you topped out your free tier on one and have some left on another. However, whether you decide to hop clouds really depends on what kind of work you want to do and whether you're willing to pay even a little bit for it.

It turns out that GCP has a really good free tier when it comes to citizen science. AWS and Azure do not include their equivalents to BigQuery in their free tier, even at a trial or limited time level. However, the prices are generally small enough that, if you're very careful about optimization, runtime, cold start times (for serverless), and destruction immediately after getting what you need, you probably are only looking at under USD$100 of calculations.

For the purposes of this workshop, though, we're trying to stay in the free tier. And there are a lot of ways to do the work we want to do in a serverless function so long as we get the majority of the big data work done on GCP.

## Thinking in terms of interchangeable components

The great thing about thinking in terms of cloud engineering and IaC is we can break things up and run bits and pieces of our workflow on different clouds. We don't need to stick to one spot for everything. So, if you realize you understand the query system on GCP better but want to run your functions on Azure, you can do that.

For the next part of the workshop, we're breaking things down. In general, we have data and file storage, a data analytics engine, and a serverless function. The data analytics engine is the resource-intensive part, so we're going to use GCP's free tier for that (which is why we saved that file). But we can create data storage and run a serverless function on other clouds! We'll do the first one on AWS.

## Building our AWS infra

### Lambda considerations

AWS Lambda functions have some small quirks to deal with when working with data science scenarios with Python (or really any language that relies on external dependencies). They do not generally come with the ability to add dependent libraries, like `pandas` or `flask`, on creation. Unless, however, you either containerize the application (which Lambda now supports) or use something called Layers. We'll explore Layers in our code as it's the easier of the two, but also the more not-intuitive if you've never used it before.

We're going to need to use ARNs, or Amazon Resource Names, to identify some stuff. We'll look at those when we get there. But we also can build custom Layers in our IaC code, so we might even get to explore that today!

### Adding Code

Remember that CSV file that we pulled down from GCP? We're going to upload it to S3 as part of building up our infrastructure.

We also need to modify our application code! We'll talk about why, but copy the `aws_main.py` file into your `app` directory. We'll talk about what changed live:

```python
import base64
import os
from datetime import datetime
from io import BytesIO, StringIO

import boto3
import matplotlib.pyplot as plt
import pandas

s3_client = boto3.client(service_name='s3')
result = s3_client.get_object(Bucket=f'{os.environ["BUCKET_NAME"]}', Key='laura-csv')
datadirlist = []
for line in result["Body"].read().splitlines():
    each_line = line.decode('utf-8')
    datadirlist.append(each_line)
datafile = '\n'.join(datadirlist)


def get_data(request):
    datadir = StringIO(datafile)
    haillist = []
    hailtemp = pandas.read_csv(datadir, infer_datetime_format=True, parse_dates=[0],
                               date_parser=lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S'))
    haillist.append(hailtemp)
    hailtemp["YEAR"] = pandas.to_datetime(hailtemp['event_begin_time']).dt.year
    haillist.append(hailtemp['YEAR'])
    hailtemp["BEGIN_DAY"] = pandas.to_datetime(hailtemp['event_begin_time']).dt.day
    haillist.append(hailtemp['BEGIN_DAY'])
    haildf = pandas.DataFrame().append(haillist)
    plt.figure(figsize=(20, 10))
    ax = (haildf["YEAR"].groupby(haildf["BEGIN_DAY"]).count()).plot(kind="bar", color="#805ac3", rot=0)
    ax.set_facecolor("#eeeeee")
    ax.set_xlabel('Day of Month')
    ax.set_ylabel('Frequency')
    ax.set_title('Hail in March')
    x = haildf["YEAR"].groupby(haildf["BEGIN_DAY"]).count()
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img


def lambda_handler(event, lambda_context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": f"<img src=\"data:image/png;base64,{base64.b64encode(get_data(event).read()).decode('utf-8')}\">"
    }

```

Use this skeleton code to build up the AWS infrastructure to deploy our code (or you can copy-paste and watch me live code!).

```python
import json

import pulumi_aws as aws
from pulumi import AssetArchive, FileArchive, FileAsset, ResourceOptions
from pulumi import export as key_export

# 1. Copy GCS bucket to S3 (export.csv; 2.6kb for the hail example).
# The issue is Athena isn't in free tier, so we're blending the "labs" to make one lab on multiple clouds.
data_bucket = aws.s3.Bucket()

data_object = aws.s3.BucketObject()

# 2. Run a Lambda that does the same pandas/matplotlib calculations and serves via a function URL
lambda_policy_document = aws.iam.get_policy_document()

iam_for_lambda = aws.iam.Role()

# Create the role for the Lambda to assume
lambda_role = aws.iam.Role()

role_policy_attachment = aws.iam.RolePolicyAttachment()
role_policy_attachment_2 = aws.iam.RolePolicyAttachment()

s3fs_layer = aws.lambda_.LayerVersion()

fsspec_layer = aws.lambda_.LayerVersion()

function = aws.lambda_.Function()

function_url = aws.lambda_.FunctionUrl()

key_export("function-url", function_url.function_url)
```

**Q:** Why don't we have a query?

**Q:** You may have seen other people using an API Gateway. What's the difference here between the API Gateway and Lambda Function URLs?

**Q:** What if I wanted to go to Azure instead? (Hint: What components of our data lab do you need?)

## Cleaning up

Before we finish up, we should tear everything down so we don't incur fees or go over our free tier. This is why it's so great to have IaC!

Run `pulumi destroy`, and then select `yes` in the terminal. That's it! Ensure the command runs to completion before stepping away.

If we have some time, we can start in on [experimental Lab 4](../lab-04/)!

If we don't have time, thanks for coming! Let me know what you thought about the workshop either by filling out the surveys sent via KCDC (I'll put the slide up with the QR code in a few minutes), using the tokens on the table, or contacting me through any of the contact methods on [my Linktree](https://linktr.ee/nimbinatus). Excited to meet you again sometime!