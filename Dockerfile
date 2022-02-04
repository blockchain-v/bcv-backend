FROM python:3.8.12

ADD . /bcv-backend/

WORKDIR /bcv-backend

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "openapi_server"]