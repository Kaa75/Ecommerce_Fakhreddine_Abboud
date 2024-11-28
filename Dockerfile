FROM python:3.12-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose ports for each service
EXPOSE 8000 8001 8002 8003

# Start multiple services
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 & uvicorn src.main:app --host 0.0.0.0 --port 8001 & uvicorn src.main:app --host 0.0.0.0 --port 8002 & uvicorn src.main:app --host 0.0.0.0 --port 8003"]