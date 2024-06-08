# Use the official continuumio/miniconda3 image from Docker Hub
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget default-jdk unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download the project from GitHub
RUN wget https://github.com/itsNileshHere/Microsoft-Future-Ready-Talent-Virtual-Internship-Project/archive/refs/heads/main.zip && \
    unzip main.zip && \
    mv Microsoft-Future-Ready-Talent-Virtual-Internship-Project-main/* . && \
    rm -rf Microsoft-Future-Ready-Talent-Virtual-Internship-Project-main main.zip

# Create the conda environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate the conda environment
SHELL ["conda", "run", "-n", "bioactivity", "/bin/bash", "-c"]

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["conda", "run", "-n", "bioactivity", "python", "app/app.py"]
