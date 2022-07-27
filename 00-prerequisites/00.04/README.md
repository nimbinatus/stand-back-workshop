# Lab 00.04: Setting up the CLI/SDK for your cloud provider

Pulumi and other infrastructure-as-code tools often use the CLI or SDK from the provider to authenticate. For AWS and GCP, that's the case. Let's set those up.

## AWS

1. [Create an IAM user in the AWS console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) with programmatic access and ensure it has sufficient permissions to deploy and manage your Pulumi program’s resources.
1. [Set up AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) for your user.
    > **Note:** If you are using temporary security credentials, you will also have to supply an AWS_SESSION_TOKEN value before you can use Pulumi to create resources on your behalf.
    > Your AWS credentials are never sent to pulumi.com. Pulumi uses the AWS SDK and the credentials in your environment to authenticate requests from your computer to AWS.

You have two options for configuration: environment variables or a credentials file. As we're working with our local machine on our own profile, we'll create a credentials file.

1. [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html).
1. Configure your [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config).

    ```
    $ aws configure
    AWS Access Key ID [None]: <YOUR_ACCESS_KEY_ID>
    AWS Secret Access Key [None]: <YOUR_SECRET_ACCESS_KEY>
    Default region name [None]: <YOUR_AWS_REGION>
    Default output format [None]:
    ```

    Your AWS credentials file is now located in your home directory at `.aws/credentials`.

    You can also create the shared credentials file by hand. For example:

    ```
    [default]
    aws_access_key_id = <YOUR_ACCESS_KEY_ID>
    aws_secret_access_key = <YOUR_SECRET_ACCESS_KEY>
    ```

## GCP

To provision resources with the Pulumi Google Cloud Provider, you need to have Google credentials.

When developing locally, Pulumi recommends that you install the [Google Cloud SDK](https://cloud.google.com/sdk/install) and then [authorize access with a user account](https://cloud.google.com/sdk/docs/authorizing#authorizing_with_a_user_account). If `gcloud` is not configured to interact with your Google Cloud project, set it with the `config` command using the project’s ID:

```bash
$ gcloud config set project <YOUR_GCP_PROJECT_ID>
```

 Next, Pulumi requires default application credentials to interact with your Google Cloud resources, so run `auth application-default login command` to obtain those credentials.
 
 ```bash
 gcloud auth application-default login
 ```
