# Lab 2: Adding Applications and Data Analysis

Let's start out with a number-crunching app that takes in years' worth of data and discovers the most likely day for hail in Austin, TX, in March.

## Application 1: A crash course in pandas

Now, we're going to build our first application with matplotlib and pandas. Sometimes, the biggest part of scientific computing is parsing large datasets. The pandas library helps us by allowing us to put a structure around large datasets of varying formats and then manipulate that data. The matplotlib plots data in visually appealing formats.

We'll spend a bit of time talking about pandas and matplotlib, along with numpy and SciPy, here.

### The scenario

[![Austin KVUE](https://img.youtube.com/vi/Dqgl2VK4u8E/0.jpg)](https://www.youtube.com/watch?v=Dqgl2VK4u8E)

In Austin, TX, there's a persistent rumor that the most likely day for hail is March 25, to the point that, even if no hail is forecast, people go park their cars in random parking garages or cover their cars in foam pool toys in a superstitious attempt to ward off damage. Is it true? What's happened there in the past 50 years? Let's find out.

### Our first application

Remember that `app` directory where we have `gcp_test.py`? We're going to add a new file, `main.py`, that has our actual pandas/matplotlib application. First, we need a `requirements.txt` file:

_app/requirements.txt_
```
matplotlib
pandas
fsspec
tox
tox-conda
gcsfs
```

Now, since this *isn't* a workshop about pandas, matplotlib, and SciPy, we can copy code here. We'll go through this live, though, so don't worry! Copy this into a new file called `main.py`:

_app/main.py_
```python
import os
from io import BytesIO
import flask
import pandas
import matplotlib.pyplot as plt
from datetime import datetime


def get_data(request):
    datadir = f"{os.environ['DATA']}"
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
    return flask.send_file(img, mimetype='image/png')
```

Here's what your file structure should look like:

```
<root>/
    app/
        main.py
        requirements.txt
        gcp_test.py
    infra/
        venv/
            ...
        __main__.py
        Pulumi.dev.yaml
        Pulumi.yaml
        requirements.txt
    .gitignore
    sql_query.sql
```

We already have the SQL query, but let's go through that:

```sql
SELECT
    event_begin_time,
    magnitude,
    EXTRACT(MONTH FROM event_begin_time) as month
FROM
    `bigquery-public-data.noaa_historic_severe_storms.storms_*`
WHERE
    state LIKE 'Texas'
    AND cz_name LIKE 'TRAVIS'
    AND event_type LIKE 'hail'
    AND EXTRACT(MONTH FROM event_begin_time) = 3
```

**Q:** Now, we have to update our cloud function infra component to call the new file, and we need to pass in that `DATA` environment variable. How can we do that? (P.S. - The answer is in the `code/gcp-infra.py` file, but try to figure it out first!)

### Run it!

You'll note that, when you run the `pulumi up` command again, it runs much faster this time. In fact, it only updates the cloud function component rather than updating or re-creating everything.

**Q:** Why do you think that is? What does that mean for your data lab?

You may need to run it twice because the BigQuery jobs only report back that they started to IaC tools, not that they finished. So the export job sometimes runs before the data can be gathered in the query job.

**Q:** Let's talk about why that is, and how you can troubleshoot those kinds of issues in your data lab.

#### Results

Well, would you look at that. Turns out that, yes, March 25 is a very good day for hail in Austin, TX.

**Q:** However, that being said, is it likely that you'd cover your car in that scenario? Why or why not? And what are people missing in these numbers?

## Cleaning up

Now that we're done with GCP, we should tear everything down so we don't incur fees or go over our free tier. This is why it's so great to have IaC!

Before we tear everything down, download the `export.csv` file from your GCP bucket where it's living. You can do that via the terminal or the UI; it's up to you. We're going to need it later.

Once you've gotten that downloaded, the only thing you need to do is run `pulumi destroy` and then select `yes` in the terminal. That's it! Ensure the command runs to completion.

All set? Let's move on to [Lab 3](../lab-03/)!
