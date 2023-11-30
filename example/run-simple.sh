#!/bin/sh

input_file="input-10.smi"
output_prefix="mw-output"
gcs_bucket_name="<GCS bucket name>"
container_image="<Docker Hub username>/rdkit-df"

#GCP-specific settings
gcp_region="GCP region"
gcp_project="GCP project ID"
#optional network name
gcp_network_name="df"

python3 rdkit-mw.py \
       --input="gs://$gcs_bucket_name/$input_file" \
       --output="gs://$gcs_bucket_name/$output_prefix" \
       --temp_location="gs://$gcs_bucket_name/tmp" \
       --runner=DataflowRunner \
       --experiments=use_runner_v2 \
       --max_num_workers=10 \
       --machine_type=n1-standard-2 \
       --job_endpoint=embed \
       --sdk_container_image="$container_image" \
       --sdk_location=container \
       --project="$gcp_project" \
       --region="$gcp_region" \
       --network="$gcp_network_name" \
       --no_use_public_ips
