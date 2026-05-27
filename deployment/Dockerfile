# Use official lightweight Python 3.10 image
FROM python:3.10-slim

# Set environment variable to ensure python output is unbuffered
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PORT=5000

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first to leverage Docker layer caching
COPY backend/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the working directory
COPY . .

# Explicitly download NLTK datasets so they are pre-bundled in the image
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('stopwords', quiet=True)"

# Expose server port
EXPOSE 5000

# Run the production gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:app"]
