FROM keitarodxs/aia-utils:latest

WORKDIR /app

RUN apt-get update && apt-get -y install
RUN apt-get install -y wget
RUN apt-get update -y && apt-get install -y chromium
RUN echo 'export CHROMIUM_FLAGS="$CHROMIUM_FLAGS --no-sandbox"' >> /etc/chromium.d/default-flags


RUN pip install --upgrade pip

RUN pip install poetry
COPY . .
COPY pyproject.toml poetry.lock ./
RUN poetry install


CMD [ "poetry", "run", "daemon"]
