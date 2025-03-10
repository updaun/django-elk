FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.8.2

COPY ./pyproject.toml ./poetry.lock /tmp/
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

# 시스템 라이브러리 및 필요한 라이브러리 설치
RUN apk update && \
    apk add --no-cache postgresql-client libgomp libstdc++ openblas-dev curl libffi-dev && \
    apk add --no-cache --virtual .build-deps \
    g++ gcc libxml2-dev libxslt-dev \
    libc-dev linux-headers postgresql-dev musl-dev openblas-dev && \
    pip install wheel

# Poetry 설치
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

# pyproject.toml과 poetry.lock 파일을 /app 디렉토리로 이동
RUN mv /tmp/pyproject.toml /tmp/poetry.lock /app/
RUN poetry config virtualenvs.create false

# 가상 환경 설정 및 Python 패키지 설치
RUN poetry install --no-interaction --no-ansi

# 불필요한 파일 제거 및 가상 패키지 삭제
RUN rm -rf /tmp && \
    apk del .build-deps

# 사용자 설정
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
