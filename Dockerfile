FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
ENV LISTEN_PORT 5001
EXPOSE 5001
COPY ./app /app
RUN pip install -r requirements.txt
ENV STATIC_PATH /app/app/static
