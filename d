FROM python:3.11-slim

WORKDIR /app



# Copy requirements first for better caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

EXPOSE 5000

# Use gunicorn for production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]