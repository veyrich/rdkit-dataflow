# RDKit in Dataflow

## Introduction

During the preparation of scientific data one often has to apply multiple data transformations. There are many data processing environments that facilitate the application of these transformations. [Google Cloud’s Dataflow](https://cloud.google.com/dataflow) - based on the open-source Apache Beam programming model - can be particularly useful in this context. It is capable and robust, scales seamlessly and requires essentially no setup or maintenance.

The Google Cloud Dataflow SDK for Python allows one to write Dataflow pipelines in Python. By default only standard Python libraries are available though. In order to use additional non-standard libraries or custom third party code (incl. native code) one can build a custom Dataflow container and in turn get access to an essentially limitless amount of additional functionality from within the fully managed Dataflow environment.

The container build process is fairly straightforward and is documented in detail [here](https://cloud.google.com/dataflow/docs/guides/using-custom-containers). See the “container” folder for an actual example utilizing [RDKit](https://www.rdkit.org/), a comprehensive and versatile toolkit for cheminformatics.

## Example

In this example we calculate the molecular weight for a given chemical compound (specified as a SMILES string). The actual code is deliberately kept very very simple in order to illustrate the key point. Most scientific data processing pipelines will of course be substantially more complex and the code implementing the data transformations will in turn be more complex as well.

### Building the container

The [Dockerfile](https://github.com/veyrich/rdkit-dataflow/blob/main/container/Dockerfile) for the custom container is very straightforward. We start with Debian 11, apply OS updates, and install the precompiled RDKit packages available via Debichem. We then install the Apache Beam SDK for GCP. Note that Dataflow is looking for ‘python’ rather than python3’. Previous versions of the Beam SDK would fail rather silently if ‘python’ was not available making debugging somewhat challenging. More recent versions offer more verbose error messages. Note also that the major/minor python versions need to match between the custom container and the beam runtime environment included in the container. Debian 11 currently comes with Python 3.9.2 so we install apache/beam_python3.9_sdk.

Due to a memory leak in versions 2.47.0 - 2.50.0 of the Beam Python SDK, we use a slightly older version of the SDK (2.46.0). See SDK version support status for details on which version is supported until when.

Please note that the local environment from which one launches a Dataflow job, also needs to have the relevant Apache Beam packages installed (either system-wide or in a virtualenv).


### Running a pipeline

Running the Dataflow pipelines from the command line is quite simple. A sample command line looks as follows (see the [run-simple.sh](https://github.com/veyrich/rdkit-dataflow/blob/main/example/run-simple.sh) script for more details on how to set the required variables for input, output, etc):

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


The above command line will submit the Dataflow job to the GCP-hosted execution engine. Scaling of the resources used for the Dataflow job is handled automatically by the Dataflow execution engine (we only set a maximum for the number of workers, e.g. 10 in this case). Additional information on pipeline options is available [here](https://cloud.google.com/dataflow/docs/guides/setting-pipeline-options)
