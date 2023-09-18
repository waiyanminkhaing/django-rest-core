FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1

# pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.dev.txt /tmp/pip-tmp/
RUN pip --no-cache-dir install -r /tmp/pip-tmp/requirements.dev.txt
RUN rm -rf /tmp/pip-tmp
