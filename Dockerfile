# Use an official Python runtime as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . /app

# By default, run the auth_app.py
CMD ["python", "auth_app.py"]