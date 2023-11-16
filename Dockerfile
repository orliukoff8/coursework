FROM python:3.8.13-slim-buster

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH=/app

WORKDIR /app

COPY ./ /app

EXPOSE 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

#docker run -p 8000:80 coursework