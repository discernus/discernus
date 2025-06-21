# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Set the PYTHONPATH environment variable to include the src directory
# This ensures that imports from `narrative_gravity` work correctly everywhere.
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Define the entrypoint for the container.
# This makes the container executable, running the orchestrator by default.
ENTRYPOINT ["python3", "scripts/applications/comprehensive_experiment_orchestrator.py"]

# Set a default command (e.g., to show help if no arguments are passed)
CMD ["--help"] 