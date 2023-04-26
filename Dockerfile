FROM python:3.9-slim-buster

WORKDIR /main

COPY . /main

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]
