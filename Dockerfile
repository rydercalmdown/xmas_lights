FROM python:3.8
WORKDIR /code
COPY server/requirements.txt .
RUN pip install -r requirements.txt
COPY server .
ENV PYTHONUNBUFFERED=1
CMD ["sh", "-c", "gunicorn --workers=1 --log-level DEBUG -b 0.0.0.0:$PORT wsgi"]
