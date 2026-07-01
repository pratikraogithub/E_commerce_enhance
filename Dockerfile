# Use Python Image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run server
CMD [ "python", "manage.py", "runserver", "0.0.0.0.8000" ]