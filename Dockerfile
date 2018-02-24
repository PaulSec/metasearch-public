FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
WORKDIR /code/app
CMD ["python", "main.py"]