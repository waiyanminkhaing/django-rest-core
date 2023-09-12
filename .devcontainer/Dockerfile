FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1

# pip
ARG DEV=false

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.dev.txt /tmp/pip-tmp/
RUN if [ $DEV = "true" ]; then pip --no-cache-dir install -r /tmp/pip-tmp/requirements.dev.txt ; fi
RUN rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
