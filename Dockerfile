FROM python:3.6-slim
COPY ./app /app
WORKDIR /app
RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential
RUN pip install -Ur requirements.txt
RUN usermod -u 1000 www-data
RUN usermod -G staff www-data
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]