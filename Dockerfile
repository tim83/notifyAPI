FROM docker.io/library/python

COPY . /app

WORKDIR /app
RUN pip install .
ENTRYPOINT [ "python" ]
CMD ["app.py"]
