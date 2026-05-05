FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app

# Install dependencies (root AI packages + backend-specific packages)
COPY requirements.txt ./
COPY app/backend/requirements.txt ./backend-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r backend-requirements.txt

# Copy full project (backend imports from src/)
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
