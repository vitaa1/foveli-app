FROM python:3.13-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home app
COPY --chown=app:app . .
RUN DJANGO_SECRET_KEY=build-only-placeholder-not-a-runtime-secret-0123456789-abcdefghij DJANGO_DEBUG=false python manage.py collectstatic --noinput
USER app
EXPOSE 8000
CMD ["sh", "-c", "exec gunicorn foveli.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --access-logfile -"]
