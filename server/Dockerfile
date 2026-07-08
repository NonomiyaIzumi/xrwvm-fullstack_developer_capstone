FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir django requests whitenoise gunicorn

COPY . .

RUN python manage.py collectstatic --noinput

ENV DJANGO_DEBUG=False
EXPOSE 8000

CMD ["gunicorn", "djangoproj.wsgi:application", "--bind", "0.0.0.0:8000"]
