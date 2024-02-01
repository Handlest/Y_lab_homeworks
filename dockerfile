FROM python:3.10-slim
LABEL maintainer="Handlest (Mikhalev Maxim)"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN adduser --disabled-password --gecos '' app_user

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

RUN chown -R app_user:app_user /app
USER app_user

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
