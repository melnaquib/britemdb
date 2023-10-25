FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

# ARG INSTALL_DEV=false
# RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#COPY ./app /app
COPY ./app /app/app

COPY sample.env /sample.env
COPY .env /.env
COPY docker-compose.env /docker-compose.env
COPY tests/testconf.env /testconf.env

ENV VARIABLE_NAME=api
ENV PYTHONPATH=/api;/

#ENTRYPOINT "source /.env && /start-reload.sh"
#ENTRYPOINT bash -c "source /.env && source /docker-compose.env && source /testconf.env && /start-reload.sh"
#ENTRYPOINT bash -c "source /.env && source /docker-compose.env && /start-reload.sh"
#ENTRYPOINT bash -c "source /.env && /start-reload.sh"
#ENTRYPOINT bash -c "source /sample.env && /start-reload.sh"
#ENTRYPOINT bash -c "source /sample.env && echo /start-reload.sh $PORT"
#ENTRYPOINT echo $

ENTRYPOINT ["/bin/bash", "-c", "source /sample.env && /start-reload.sh"]
