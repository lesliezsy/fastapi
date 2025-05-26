FROM python:3.9.7
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN ls -la
RUN cat requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This assumes your Dockerfile is in the root of your project
# and your application code is in a folder named 'app'
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]