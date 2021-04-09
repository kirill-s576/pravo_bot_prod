FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code/

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get --assume-yes install python3-dev libmariadb-dev build-essential
RUN sudo apt-get --assume-yes install wkhtmltopdf
RUN pip install -r requirements.txt

COPY . /code
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000