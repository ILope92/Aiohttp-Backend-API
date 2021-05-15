FROM ubuntu:20.04
RUN apt-get update -y
# Install Python

RUN apt-get install -y python3.8 \
    && ln -s /usr/bin/python3.8 /usr/bin/python3
RUN apt-get install -y python3-pip python3-dev build-essential
RUN python3.8 -m pip install pip --upgrade

COPY requirements.txt install/requirements.txt
RUN python3.8 -m pip install -r install/requirements.txt
COPY . /app
WORKDIR /app
CMD ["python3", "app_run.py"]
