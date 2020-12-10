FROM python:3.8-slim
WORKDIR /test_characters_api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./tests/ ./tests/

CMD ["pytest", "./server.py"]
