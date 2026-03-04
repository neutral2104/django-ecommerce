# Stage 1: Build dependencies
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Runtime (Under 200MB target)
FROM python:3.11-slim
WORKDIR /app

# Security: Create non-root user (Requirement 2)
RUN useradd -m django-user
USER django-user

# Copy installed packages and code
COPY --from=builder /root/.local /home/django-user/.local
COPY --chown=django-user:django-user . .

ENV PATH=/home/django-user/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Command for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce_project.wsgi:application"]
