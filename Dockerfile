FROM docker.io/library/python:3.10-bullseye

COPY ../notify /app

WORKDIR /app
RUN pip install .
ENTRYPOINT [ "python" ]
CMD ["-m", "notify.motion_api"]
