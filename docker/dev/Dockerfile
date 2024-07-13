FROM python:3.12-slim

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update -y  \
    && apt-get upgrade -y

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.8.3

# install poetry
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

# set work directory as /inspector
WORKDIR /inspector

# install dependencies
COPY poetry.lock* pyproject.toml /inspector/
RUN --mount=type=cache,target=/root/.cache/pip \
    poetry install --with=dev --no-interaction

# remove packages that are not needed anymore
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip

# copy the start script
COPY docker/dev/start /start
RUN sed -i "s/\r$//g" /start \
    && chmod +x /start

# copy project
COPY . .

# run start script
CMD ["/start"]
