# Using lightweight python image
FROM python:3.13.0

# Set working directory
WORKDIR /app

# Copy file
COPY requirements.txt .
COPY app.py . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for AWS Elastic Beanstalk
EXPOSE 8080

# Run the Gradio App
CMD ["python", "app.py"]