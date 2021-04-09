FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code/

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip

RUN apt-get update
RUN apt-get install wget
RUN apt-get --assume-yes install python3-dev libmariadb-dev build-essential
RUN cd /tmp && \
  wget -nv https://downloads.wkhtmltopdf.org/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz -O wkhtmltox.tar.xz && \
  tar -xaf wkhtmltox.tar.xz && \
  rm -f wkhtmltox.tar.xz && \
  mv wkhtmltox/bin/wkhtmlto* /usr/local/bin/
RUN pip install -r requirements.txt

COPY . /code
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000