FROM python:3.11.7

RUN pip install poetry==1.3.2
RUN pip install psycopg[binary]
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the project files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .


