FROM python:3.12-slim as requirements

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update -y  \
    && apt-get upgrade -y

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.8.3

# set work directory as /requirements
WORKDIR /requirements
# copy over the files needed for poetry
COPY poetry.lock* pyproject.toml ./

# install poetry, export requirements
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry export -f requirements.txt --output requirements.txt

# create a virtual environment and install dependencies
RUN python -m venv /venv
# set python to use the virtual environment
ENV PATH="/venv/bin:$PATH"
# install dependencies to the virtual environment
RUN --mount=type=cache,target=/root/.cache/pip \
    /venv/bin/python -m pip install -r requirements.txt

FROM python:3.12-slim

RUN apt-get update -y  \
    && apt-get upgrade -y \
    # clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 999 inspector  \
    && useradd -l -r -u 999 -g inspector inspector

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# copy over the virtual environment
COPY --from=requirements --chown=inspector:inspector /venv /venv
# set python to use the virtual environment
ENV PATH="/venv/bin:$PATH"

# set work directory as /inspector
RUN mkdir /inspector \
    && chown inspector:inspector /inspector
WORKDIR /inspector

# copy the start script
COPY --chown=inspector:inspector docker/prod/start /start
RUN sed -i "s/\r$//g" /start \
    && chmod +x /start

# copy the supervisord config and gunicorn config
COPY --chown=inspector:inspector docker/prod/gunicorn.conf.py /inspector/gunicorn.conf.py

# copy project and remove unnecessary files
COPY --chown=inspector:inspector . .
RUN rm -rf \
    .dockerignore \
    docker \
    poetry.lock \
    pyproject.toml

USER inspector

CMD ["/start"]
