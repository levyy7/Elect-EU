# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container
#COPY ../.. .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5001
EXPOSE 5001

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0" , "--port=5001"]
