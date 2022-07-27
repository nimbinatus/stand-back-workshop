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
        "statusCode": 418,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": f"<img width=\"1020\" height=\"520\" src=\"data:image/png;base64,{base64.b64encode(get_data(event).read()).decode('utf-8')}\">"
    }
