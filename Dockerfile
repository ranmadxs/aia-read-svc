FROM keitarodxs/aia:aia-utils_0.1.9
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN apt-get install -y wget
RUN apt-get update -y && apt-get install -y chromium
RUN echo 'export CHROMIUM_FLAGS="$CHROMIUM_FLAGS --no-sandbox"' >> /etc/chromium.d/default-flags


COPY . .
COPY pyproject.toml poetry.lock ./
RUN poetry install


CMD [ "poetry", "run", "daemon"]
