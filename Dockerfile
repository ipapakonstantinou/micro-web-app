FROM ubuntu

# RUN apk add --no-cache py-pip python-dev libffi-dev openssl-dev gcc libc-dev make && \
#    pip install docker-compose

RUN mkdir -p /home/test

RUN apt-get update && \
      apt-get -y install sudo


RUN sudo apt install docker.io -y
RUN sudo apt install curl -y
RUN sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN sudo chmod +x /usr/local/bin/docker-compose
RUN sudo apt install nano -y
RUN sudo apt install nginx -y

# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

# USER docker


COPY . ./home/test

EXPOSE 8080
