# Lab 4 (Bonus): Abstraction and Platform Engineering 

**IMPORTANT:** This part of the workshop is experimental. We'll build it together!

We can get actually to build out those components as abstractions in our IaC code. We can also cloud hop in a more platform-like fashion. First, you could abstract away the specific cloud-based calls to be more generic (which is why we stuck to serverless calls and storage buckets versus using specific data pipelines!). Second, you could run a program in front that allows you to choose which cloud-specific program to call. We'll do both here.

## Abstractions

## Platform engineering

Generally, to do platform engineering like this, there needs to be an API around the usual APIs that you call. Pulumi already has one, so we'll use that. If you want to build one around the APIs for different clouds, though, all of the major cloud providers do offer SDKs that you could build a program around, as do other IaC tools.

_./__main__.py_
```python
import os.path

from pulumi import automation as auto

print("Which cloud do you want to work with? Options are 'aws' or 'gcp'.")
cloud = input(u'\u2601' + " -->  ")


def set_config_vals(cloud_name):
    print("I need some configuration values.")
    stack_name = input("What stack do you want to use? -->  ")
    stack_name = stack_name
    work_dir = os.path.join(os.path.dirname(__file__), "infra", cloud_name)
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        work_dir=work_dir
    )
    if cloud_name == "aws":
        if not stack.get_config("aws:region"):
            cloud_region = input(f"What's your {cloud_name} region? -->  ")
            switch_type = input("Are you using a profile? Y/y or N/n -->  ")
            if switch_type == "Y" or switch_type == "y":
                cloud_profile = input("What's the name of your profile? -->  ")
            else:
                print("the default profile will be used")
                cloud_profile = "default"
            cloud_dict = {
                "aws:region": auto.ConfigValue(cloud_region),
                "aws:profile": auto.ConfigValue(cloud_profile),
            }
            stack.set_all_config(cloud_dict)
        return stack
    elif cloud_name == "gcp":
        if not stack.get_config("gcp:region"):
            cloud_region = input(f"What's your {cloud_name} region? -->   ")
            cloud_project = input(f"What's your {cloud_name} project? -->  ")
            cloud_zone = input(f"What's your {cloud_name} zone? -->  ")
            cloud_dict = {
                "gcp:region": auto.ConfigValue(cloud_region),
                "gcp:project": auto.ConfigValue(cloud_project),
                "gcp:zone": auto.ConfigValue(cloud_zone),
            }
            stack.set_all_config(cloud_dict)
        return stack


while cloud:
    if cloud == "aws":
        try:
            set_config_vals(cloud)
            from infra.aws import aws_datalab as aws
        except ImportError:
            raise ImportError("I can't import the custom AWS infrastructure. Is your filestructure correct?")
        pass
        break
    elif cloud == "gcp":
        try:
            set_config_vals(cloud)
            from infra.gcp import gcp_datalab as gcp_custom
            gcp_custom.run_me.id.apply(lambda i: print(i))
        except ImportError:
            raise ImportError("I can't import the custom GCP infrastructure. Is your filestructure correct?")
        # pass
        break
    else:
        print("Please enter one of the following options: aws or gcp.")
        cloud = input("☁️ -->  ")
```

Here's what your file structure should now look like:

```
<root>/
    app/
        main.py
        requirements.txt
    infra/
        aws/
            aws_datalab.py
        gcp/
            gcp_datalab.py
    venv/
        ...
    .gitignore
    __main__.py
    Pulumi.dev.yaml
    Pulumi.yaml
    requirements.txt
    sql_query.sql
```
