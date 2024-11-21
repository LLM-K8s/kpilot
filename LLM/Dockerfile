FROM docker.io/python:3.12.7-alpine3.20 as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY pyproject.toml poetry.lock ./

RUN apk add --no-cache py3-pip python3 bash && \
    pip install poetry && \
    poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --output requirements.txt


FROM docker.io/python:3.12.7-alpine3.20 as runtime

RUN apk update \
    && apk add --no-cache \
        build-base

COPY --from=base /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./LLM/

ENV OPENAI_API_KEY="your-openai-api-key" \
    OLLAMA_BASE_URL="http://localhost:11434"

EXPOSE 50051

CMD ["python", "-m", "LLM"]
