FROM python:3.11-alpine
LABEL author="xewus" version="test"
RUN mkdir /app
COPY . /app/
ENV BOT_TOKEN=$
RUN pip3 install -U pip && pip install -r /app/requirements.txt --no-cache-dir
WORKDIR /app/
CMD python3 start_app.py