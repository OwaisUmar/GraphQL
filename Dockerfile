FROM python:3.10.2-buster

# Make a directory for our application
WORKDIR /.

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy our source code
COPY QueryPoolDataAutomation.py .

# Run the application
CMD ["python", "QueryPoolDataAutomation.py"]
