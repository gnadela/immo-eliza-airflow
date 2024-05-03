# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /ml

# Copy the current directory contents into the container at /app
COPY . /ml

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run train.py when the container launches
CMD ["python", "./train.py"]
