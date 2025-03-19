# Use Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5002

# Run the Flask app
CMD ["python", "drink.py"]