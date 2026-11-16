FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCMS_DATABASE=/data/scms.sqlite3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN mkdir -p /data && useradd --create-home --uid 10001 scms \
    && chown -R scms:scms /app /data

USER scms
EXPOSE 5000

CMD ["waitress-serve", "--listen=0.0.0.0:5000", "--call", "app:create_app"]
