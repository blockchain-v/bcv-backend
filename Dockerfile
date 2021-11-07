FROM python:3-onbuild

COPY . /bcv-backend
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./api.py" ]