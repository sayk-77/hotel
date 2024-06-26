FROM python:3.12.3

WORKDIR /Hotel

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]