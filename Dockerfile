# Use a small Python base
FROM python:3.12-slim

# Set working directory inside the image
WORKDIR /app

# 1) Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy the rest of your project (includes schema/, model/, app.py, etc.)
COPY . .

# 3) Expose API port
EXPOSE 8000

# 4) Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
