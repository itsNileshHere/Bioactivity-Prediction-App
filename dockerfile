# Use the official continuumio/miniconda3 image from Docker Hub
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository
RUN git clone https://github.com/itsNileshHere/Microsoft-Future-Ready-Talent-Virtual-Internship-Project.git .

# Create and activate the conda environment
COPY environment.yml .
RUN conda env create -f environment.yml && \
    echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app/app.py"]
