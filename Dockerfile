FROM docker.io/library/python

COPY . /app

WORKDIR /app
RUN apt-get update
RUN apt-get install -y wakeonlan
RUN pip install .
ENTRYPOINT [ "python" ]
CMD ["app.py"]
