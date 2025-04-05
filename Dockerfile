# 1. Base Image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy files
COPY ./app ./app
COPY ./models ./models
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
