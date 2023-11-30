FROM debian:11

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-rdkit

RUN apt-get install -y python3-pip python3-venv virtualenv 
RUN pip3 install --no-cache-dir apache-beam[gcp]==2.46.0

#Beam is looking for 'python' (not 'python3')
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

COPY --from=apache/beam_python3.9_sdk:2.46.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT ["/opt/apache/beam/boot"]



