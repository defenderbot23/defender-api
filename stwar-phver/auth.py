from google.cloud import secretmanager

def init_auth():

    # GCP project in which to store secrets in Secret Manager.
    project_id = "start-ax"

    # ID of the secret to create.
    secret_id = "SRV_ACC_JSON"

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret_name = client.secret_version_path(project_id, secret_id, 1)

    # Access the secret version.
    response = client.access_secret_version(request={"name": secret_name})

    # Print the secret payload.
    payload = response.payload.data.decode("UTF-8")
    print(f"Plaintext: {payload}")

    return payload
