# syntax=docker/dockerfile:1
FROM python:3.7-alpine
# Sets the working directory to "code" on the Docker image
WORKDIR /code
# Sets the Flask environment variables
#ENV FLASK_APP=app.py
ENV FLASK_APP=/api/main.py
ENV FLASK_RUN_HOST=0.0.0.0
# Install gcc and other dependencies
RUN apk add --no-cache gcc musl-dev linux-headers
# All dependencies are listed in the requirements.txt file
COPY requirements.txt requirements.txt 
# pip install is run on the entire requirements list at startup of the Docker image
RUN pip install -r requirements.txt
# Set or 'open' port 5000 for the container to listen on
EXPOSE 5000
# Copy the current directory the file is in (.) to the work directory specified (.)
COPY . .
COPY ./node-manager .
# Set the default command for the container to "flask run"
CMD ["flask", "run"]