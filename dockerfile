# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository
RUN git clone https://github.com/itsNileshHere/Microsoft-Future-Ready-Talent-Virtual-Internship-Project.git .

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Expose the port the app runs on
EXPOSE 80

# Run the application
# CMD ["python", "app/app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app.app:app"]