FROM python:3.8.12

ADD . /bcv-backend/

WORKDIR /bcv-backend

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r test-requirements.txt

CMD ["python3", "-m", "openapi_server"]