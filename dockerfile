# Stage 1: Build
FROM python:3.11-slim-bullseye AS builder

# Set the working directory
WORKDIR /app

# Copy only the requirements file first for efficient caching
COPY requirements.txt .

# Install dependencies
RUN pip install --user -r requirements.txt

# Copy the rest of the application files
COPY . .

FROM python:3.11-slim-bullseye as production

WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Add Python packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy only the necessary application files
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "-m","src.app"]
