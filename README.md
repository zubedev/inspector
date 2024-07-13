```text
██╗███╗   ██╗███████╗██████╗ ███████╗ ██████╗████████╗ ██████╗ ██████╗
██║████╗  ██║██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║██╔██╗ ██║███████╗██████╔╝█████╗  ██║        ██║   ██║   ██║██████╔╝
██║██║╚██╗██║╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
██║██║ ╚████║███████║██║     ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
>------------------------------------- API for Inspecting HTTP Requests
```
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![python](https://img.shields.io/badge/python-3.12-%233776AB?style=flat-square&logo=python)](https://www.python.org)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org)
[![black](https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square&logo=stylelint)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit)](https://pre-commit.com)
[![license](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/zubedev/inspector/actions/workflows/ci.yml/badge.svg)](https://github.com/zubedev/inspector/actions/workflows/ci.yml)

## Features

- [x] See your own IP address
- [x] IP address to Country
- [x] Inspect HTTP headers

## Usage

```bash
# Copy the example environment file to .env
# For development you should set DEBUG=True
cp .env.example .env

# Build the docker image and run the container
docker-compose up --build --detach
```
API is now available at http://localhost:8888 (by default) - host and port can be changed in `.env`.

## Endpoints

- [root](http://localhost:8888/): `/` - See application info
- [headers](http://localhost:8888/headers): `/headers` - See HTTP request headers
- [country](http://localhost:8888/country): `/country` - See country of IP address

Schema documentation is available through **Swagger** and **ReDoc**:

- [swagger](http://localhost:8888/docs): `/docs` - Swagger UI
- [redoc](http://localhost:8888/redoc): `/redoc` - ReDoc UI

## Development

```bash
# Poetry is required for installing and managing dependencies
# https://python-poetry.org/docs/#installation
poetry install

# Run the application
poetry run python main.py

# Install pre-commit hooks
poetry run pre-commit install

# Formatting (inplace formats code)
poetry run black .

# Linting (and to fix automatically)
poetry run ruff .
poetry run ruff --fix .

# Type checking
poetry run mypy .
```

Configuration details can be found in [pyproject.toml](pyproject.toml).

## Support
[![Paypal](https://img.shields.io/badge/Paypal-@MdZubairBeg-253B80?&logo=paypal)](https://paypal.me/MdZubairBeg/10)
