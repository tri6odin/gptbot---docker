# Use an official Python runtime as the base image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /gptbot

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /gptbot

# Expose the port that the application will run on
EXPOSE 5000

# Run the command to start the application
CMD ["python", "main.py"]