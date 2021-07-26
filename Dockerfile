FROM python:3.6-slim
WORKDIR /app
COPY . .
RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential
RUN pip install -Ur requirements.txt
CMD ["python", "Run.py"]