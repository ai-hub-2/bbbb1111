FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && \
	pip install --no-cache-dir gunicorn

COPY . /app

EXPOSE 9090
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:9090", "app:app"]