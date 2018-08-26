FROM python:3.6

RUN apt-get update
RUN apt-get install -y build-essential 
RUN apt-get install -y python-dev 
RUN apt-get install -y libasound2
RUN apt-get install -y python-gi 
RUN apt-get install -y python-gi-cairo 
RUN apt-get install -y python3-gi 
RUN apt-get install -y python3-gi-cairo 
RUN apt-get install -y gir1.2-gtk-3.0
RUN apt-get install -y libcairo2-dev 
RUN apt-get install -y libgirepository1.0-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install git+https://github.com/dpallot/simple-websocket-server.git
RUN pip install --no-cache-dir -r requirements.txt
