FROM python:3.12.6-slim

WORKDIR /home/python_web_app

RUN apt-get update && \
    apt-get install -y  default-libmysqlclient-dev gcc pkg-config

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x ./start_server.sh

CMD ["./start_server.sh"]