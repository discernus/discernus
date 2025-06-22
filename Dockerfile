# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Chrome for Kaleido visualization support (multi-architecture)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && ARCH=$(dpkg --print-architecture) \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && (apt-get install -y google-chrome-stable || apt-get install -y chromium-browser || apt-get install -y chromium) \
    && rm -rf /var/lib/apt/lists/*

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