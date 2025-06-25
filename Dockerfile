FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

RUN poetry add uvicorn
RUN poetry add pydantic[email]
RUN pip install python-multipart

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 fast_one.app:app

# docker build -t "fast_one" .
# docker run -it --name fastoneapp -p 8000:8000 fast_one:latest
# docker stop fastoneapp
# docker rm fastoneapp

# docker run -d \
#     --name app_database \
#     -e POSTGRES_USER=app_user \
#     -e POSTGRES_DB=app_db \
#     -e POSTGRES_PASSWORD=app_password \
#     -v pgdata:/var/lib/postgresql/data \
#     -p 5432:5432 \
#     postgres
