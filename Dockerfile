FROM python:3.9
ARG PY_API_ID
ARG PY_API_HASH
ARG PY_PHONE_NUMBER
ARG PY_CHANNEL_USERNAME
ARG PY_DATABASE_URL
ARG PY_SESSION
ARG REDIS_HOST
ARG REDIS_PWD

ENV PY_API_ID=$PY_API_ID
ENV PY_API_HASH=$PY_API_HASH
ENV PY_PHONE_NUMBER=$PY_PHONE_NUMBER
ENV PY_CHANNEL_USERNAME=$PY_CHANNEL_USERNAME
ENV PY_DATABASE_URL=$PY_DATABASE_URL
ENV PY_SESSION=$PY_SESSION
ENV REDIS_HOST=$REDIS_HOST
ENV REDIS_PWD=$REDIS_PWD

EXPOSE 8080
WORKDIR /flat_service
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]

