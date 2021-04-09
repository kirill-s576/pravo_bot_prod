FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code/

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip

RUN apt-get update
RUN apt-get --assume-yes install python3-dev libmariadb-dev build-essential
RUN wget https://s3.amazonaws.com/shopify-managemant-app/wkhtmltopdf-0.9.9-static-amd64.tar.bz2
RUN tar xvjf wkhtmltopdf-0.9.9-static-amd64.tar.bz2
RUN mv wkhtmltopdf-amd64 /usr/local/bin/wkhtmltopdf
RUN chmod +x /usr/local/bin/wkhtmltopdf
RUN pip install -r requirements.txt

COPY . /code
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000