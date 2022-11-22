FROM python:latest

WORKDIR /app
RUN pip3 install aiogram
RUN pip3 install flask
RUN pip3 install flask-cors
RUN pip3 install pydantic
COPY . ./
CMD [ "python3", "main.py"]
