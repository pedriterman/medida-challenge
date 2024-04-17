# Use the official Python image as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . /app

# Expose the port on which your Flask app will run
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]