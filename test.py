import os
from airflow.models.connection import Connection


conn = Connection(
    conn_id="aws_connection",
    conn_type="aws",
    login="AKIAYRRDYOCO2JM5QC27",  # Reference to AWS Access Key ID
    password="cmP1/aUVF0Ds3c+GZIOhqzsbzT18XGJYcGfNVGo5",  # Reference to AWS Secret Access Key
    extra={
        # Specify extra parameters here
        "region_name": "ap-south-1",
    },
)

# Generate Environment Variable Name and Connection URI
env_key = f"AIRFLOW_CONN_{conn.conn_id.upper()}"
conn_uri = conn.get_uri()
print(f"{env_key}={conn_uri}")
# AIRFLOW_CONN_SAMPLE_AWS_CONNECTION=aws://AKIAIOSFODNN7EXAMPLE:wJalrXUtnFEMI%2FK7MDENG%2FbPxRfiCYEXAMPLEKEY@/?region_name=eu-central-1

# Test connection
os.environ[env_key] = conn_uri
print(conn.test_connection())
