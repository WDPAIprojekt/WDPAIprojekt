# Use an official Python image
FROM python:3.10-slim

# Set an environment variable for where the venv will live
ENV VENV_PATH=/opt/venv

# Create a virtual environment
RUN python -m venv $VENV_PATH

# Ensure commands run inside the venv
ENV PATH="$VENV_PATH/bin:$PATH"

# Create a directory for your app
WORKDIR /app

# Copy only requirements.txt first to leverage Docker's layer caching
COPY requirements.txt /app/

# Install Python dependencies inside the venv
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose port 8000 for development
EXPOSE 8000

# Optionally run migrations or any other commands as needed
CMD ["/bin/sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
