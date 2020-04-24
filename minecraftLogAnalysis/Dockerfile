FROM python:latest

# Create a directory named flask
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything to flask folder
COPY ./scripts ./scripts

EXPOSE 5000

CMD [ "python", "./scripts/app.py" ]