FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /my_site
WORKDIR /my_site
ADD . /my_site/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install mysqlclient
COPY . /my_site/