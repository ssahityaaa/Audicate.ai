FROM python:3.9

WORKDIR /app

COPY . /app
COPY . /daimn-418605-firebase-adminsdk-z1llb-b1e6f5ecc5.json

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]