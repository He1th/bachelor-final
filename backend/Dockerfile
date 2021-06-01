FROM python:3.7

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U flask-cors

COPY . .

CMD [ "python", "-u", "./Main.py" ]