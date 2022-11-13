FROM docker.io/library/python:3.10-bullseye

COPY . /app

WORKDIR /app
RUN pip install .
ENTRYPOINT [ "python" ]
CMD ["app.py"]
