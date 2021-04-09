FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code/

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip

RUN apt-get update
RUN apt-get upgrade
RUN apt-get --assume-yes install python3-dev libmariadb-dev build-essential
RUN wget -O /wkhtmltox-0.12.1_linux-wheezy-amd64.deb https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.1/wkhtmltox-0.12.1_linux-wheezy-amd64.deb
RUN dpkg -i /wkhtmltox-0.12.1_linux-wheezy-amd64.deb
RUN pip install -r requirements.txt

COPY . /code
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000