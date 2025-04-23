FROM python:3.12-alpine
LABEL authors="papanda"

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

EXPOSE 8000

CMD ["python", "app.py"]