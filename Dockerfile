FROM python:3.9

WORKDIR /app

RUN pip install --no-cache-dir flask psycopg2-binary python-dotenv

COPY . .

# Exposer le port 5001
EXPOSE 5001

CMD ["python", "server.py"]
