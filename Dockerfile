FROM python:3.6

WORKDIR /tp4

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY templates .

EXPOSE 5000
CMD python3 app.py