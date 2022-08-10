# Lab 1: Basic Infrastructure

Now that we've explored the basics of understanding all of the various cloud providers and their options, let's actually put some infrastructure together.

The major clouds all offer free access to datasets from major governmental and scientific bodies, like the National Oceanic and Atmospheric Administration (NOAA). The great thing about that is the access doesn't count against your free tier most of the time (though be sure to read the fine print!).

We will be working in the terminal and your IDE. The following commands are run in a Unix-like environment. If you're running a different environment, please reach out to ask how to modify the commands.

- [Create a project](#create-a-project)
- [Add some code](#add-some-code)

## Create a project

1. Create a directory and change into it:
    
    ```bash
    mkdir stand-back-workshop-kcdc-2022
    ```
    and
    ```bash
    cd stand-back-workshop-kcdc-2022
    ```
    
1. Now, use the `pulumi new` command to create all of the various files you'll need to get started with infrastructure as code with Pulumi:

    ```bash
    pulumi new python -y
    ```
    
    This command will print output similar to the following example with a bit more information and status as it goes:

    ```shell
    Created project 'iac-workshop'
    Created stack 'dev'
    Saved config
    Installing dependencies...
    Finished installing dependencies
    
    Your new project is ready to go!
    ```

    This command has created all the files we need, initialized a new stack named dev (an instance of our project), built a virtual environment, and installed the needed package dependencies from PyPi.

1. Let's explore the new files:

    - `__main__.py`: your program’s main entrypoint file
    - `requirements.txt`: your project’s Python dependency information
    - `Pulumi.yaml`: your project’s metadata, containing its name and language
    - `venv`: a virtualenv for your project

    Run `cat __main__.py` to see the contents of your project’s empty program:

    ```python
    """A Python Pulumi program"""
    
    import pulumi
    ```

    Feel free to explore the other files, although we won’t be editing any of them by hand.

## Configure your environment

We have to set Pulumi up to use the cloud provider of your choice. First, though, as we're using Python, we need to activate our virtual environment on our machine. The `pulumi new` command uses the built-in Python virtual environment package and sets it all up for us, so all we need to do is run this command to activate it:

```bash
source venv/bin/activate
```

For this workshop, we're working with AWS and GCP. However, due to constraints around free tiers, we're going to be doing GCP first (you'll get more information on that as we go). Let's add the necessary SDKs we need. First, add `pulumi-aws` and `pulumi-gcp` to the `requirements.txt` file (each on a new line). Then, we'll install them:

```bash
pip install -r requirements.txt
```

Now, we need to add configuration values for both clouds. First, let's do AWS.

### AWS config

Configure the AWS region you would like to deploy to:

```bash
pulumi config set aws:region us-west-2
```

If you're using an AWS profile other than the default one, we'll add that as a configuration value, too:

```bash
pulumi config set aws:profile <profile-name>
```

### GCP config

Configure the GCP project, region, and zone:

```bash
pulumi config set gcp:project <project-id>
```
```bash
pulumi config set gcp:region <region>
```
```bash
pulumi config set gcp:zone <zone>
```

## Add some code

Next, we'll add some code! We're going to add the infrastructure code for some basic data analysis. Once we're sure that's up, we'll add the actual data analysis application and hook everything together to run our first application.

For our first build, we're going to work with GCP, and we'll start with a minimal app to test our cloud function.

Set up your directories as follows, copying `gcp_test.py` and `sql_query.sql` from the `code` directory in this repo:

```
stand-back-workshop-kcdc-2022/
    app/
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

### GCP code

The full code can be found in `code/gcp_infra.py`. If you want to copy-paste and then watch and listen as I code it live, you can. However, if you want to, you can build it up with me. Either way, we'll go through the entire file line-by-line. Here's the skeleton for `__main__.py` file; I've done the first two already:

<!-- TODO: Suggestion from Waldo: Let them copy, then go through lines, versus live coding together. Also comment out all code and put it all in here, including the app. -->
```python
import secrets
import string
import time
import pulumi
import pulumi_gcp as gcp

# This query will be important later.
with open('../sql_query.sql') as f:
    my_query = f.read()

# There's a spot where you'll need to use this random string!
gen = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))

# Make a GCP storage bucket (GCS).
bucket = gcp.storage.Bucket(
    "code-bucket",
    location="US"
)

# Add an object to the bucket.
archive = gcp.storage.BucketObject(
    "code-archive",
    bucket=bucket.name,
    source=pulumi.FileArchive("../app")
)

# Make a bucket for the end dataset.
storage = gcp.storage.Bucket()

# Create a dataset for bigquery.
bar = gcp.bigquery.Dataset()

# You'll need a bigquery table.
foo = gcp.bigquery.Table()

# And now, a bigquery job to run the SQL query! Ensure you call the public dataset so you don't incur fees.
job = gcp.bigquery.Job()

# And we need a job to export the query results to s3 as a CSV for our cloud function.
export = gcp.bigquery.Job()

# Now, a function! We'll be using this to run pandas against the CSV, eventually, but for now, use the `test_app.py` file from the `code` directory.
function = gcp.cloudfunctions.Function()

# And for all cloud stuff, we always need to build up access permissions.
run_me = gcp.cloudfunctions.FunctionIamMember()

# Finally, we'll export two values to come out on the command line.
pulumi.export("bucket-url", storage.url)
pulumi.export("function-url", function.https_trigger_url)
```

Let's also explore the test app:

```python
def get_data(request):
    return "Hello, world!"
```

We'll explore the SQL query later.

## Provision infrastructure for the first time

Then, we'll provision our first bits of infrastructure.

From your terminal, ensure you're in the correct directory, which is the one where your `Pulumi.yaml` and `__main__.py` live:

```bash
$ pwd
<directories...>/stand-back-workshop-kcdc-2022
$ ls -la
total 40
drwxr-xr-x   9 nimbinatus  staff   288 Mar 25 17:35 .
drwxr-xr-x  13 nimbinatus  staff   416 May 25 11:07 ..
-rw-r--r--   1 nimbinatus  staff    12 Mar 25 17:35 .gitignore
-rw-r--r--   1 nimbinatus  staff   212 Mar 25 17:35 Pulumi.dev.yaml
-rw-r--r--   1 nimbinatus  staff    81 Mar 25 17:35 Pulumi.yaml
-rw-r--r--   1 nimbinatus  staff  2749 Mar 25 17:35 __main__.py
-rw-r--r--   1 nimbinatus  staff    32 Mar 25 17:35 requirements.txt
drwxr-xr-x   6 nimbinatus  staff   192 Mar 19 14:26 venv
```

Next, we'll stand up the infrastructure with the CLI:

```
$ pulumi up
...
```

The first time standing it up might take a little while!

When you head to the endpoint, you should get "Hello, world!" in return.

<br/>

## Cleaning up

Before we go on break, we should tear everything down so we don't incur fees or go over our free tier. This is why it's so great to have IaC! The only thing you need to do is run `pulumi destroy` and then select `yes` in the terminal. That's it! Ensure the command runs to completion before stepping away.

Now, let's take a quick break, then on to [lab 2](../lab-02/), where we get into adding the app to our infrastructure!
