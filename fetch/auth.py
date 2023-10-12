import os
import json

from google.cloud import secretmanager


def get_srv_acc_cred_json():

    # GCP project in which secrets are stored
    project_id = 'fair-alliance-401708'         # os.environ['GOOGLE_PROJECT_ID']

    # ID of the secret
    secret_id = "SECRET_GOOGLE_SRV_ACC_JSON"    # os.environ['SECRET_GOOGLE_SRV_ACC_JSON']

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret_name = client.secret_version_path(project_id, secret_id, "1")

    # Access the secret version
    response = client.access_secret_version(request={"name": secret_name})

    # Print the secret payload.
    payload = response.payload.data.decode("UTF-8")

    return payload


def dump_creds_to_file(filename):

    try:

        # get secret
        secret_value = get_srv_acc_cred_json()
        secret_json = json.loads(secret_value)

        # dump to file
        with open(filename, "w") as outfile:
            outfile.write(secret_json)

    except Exception as ex:
        print(ex)
