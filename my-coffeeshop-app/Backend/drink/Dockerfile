# # Use Python base image
# FROM python:3.9-slim

# # Set working directory
# WORKDIR /app

# # Copy only the requirements file first to leverage Docker layer caching
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Create a non-root user for security
# RUN adduser --disabled-password --gecos "" appuser
# USER appuser

# # Expose the port the app runs on
# EXPOSE 5002

# # Run the app using Gunicorn for production
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "drink:app"]


FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./drink.py .
CMD [ "python", "./drink.py" ]