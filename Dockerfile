FROM python:3.11.7
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN apt-get install -y wget
RUN apt-get update -y && apt-get install -y chromium



COPY . .
COPY pyproject.toml poetry.lock ./
RUN poetry install

CMD [ "poetry", "run", "daemon"]
