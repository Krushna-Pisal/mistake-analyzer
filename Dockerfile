FROM python:3.10-slim

WORKDIR /app

# Copy dependency manifest first for layer caching
COPY requirements.txt .

# Install all dependencies (includes openai, fastapi, uvicorn, requests)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]