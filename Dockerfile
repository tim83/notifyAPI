FROM docker.io/library/python:3-bulleye

COPY . /app

WORKDIR /app
RUN pip install .
ENTRYPOINT [ "python" ]
CMD ["app.py"]
