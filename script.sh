#!/bin/bash


cd /usr/src/books
npm start &

cd /usr/src/web
npm start &


# FROM ubuntu:12.04
#
RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker
# CMD /bin/bash

# FROM mongo
# EXPOSE 27017
#
# FROM node:latest
# RUN mkdir -p /usr/src/web
# WORKDIR /usr/src/web
# COPY ./web/package.json .
# RUN npm install --production
# COPY ./web ./
# EXPOSE 3000
# CMD npm start
#
# RUN mkdir -p /usr/src/books
# WORKDIR /usr/src/books
# COPY ./books/package.json .
# RUN npm install --production
# COPY ./books ./
# EXPOSE 3001
# CMD npm start
#
# RUN mkdir -p /usr/src/search
# WORKDIR /usr/src/search
# COPY ./search/package.json .
# RUN npm install --production
# COPY ./search ./
# EXPOSE 3003
# CMD npm start


FROM nginx
COPY ./web/public /srv/www/static
COPY ./default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080




#WORKDIR /usr/src
#COPY script.sh .
#RUN chmod +x script.sh
#ENTRYPOINT ["bash", "script.sh"]
# # RUN sudo apt-get install \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg2 \
#     software-properties-common -y
# RUN sudo apt-get install docker-ce docker-ce-cli containerd.io -y



# RUN chmod +x script.sh

# ENTRYPOINT ["sh", "script.sh"]




# docker run --rm -it -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock docker/compose:1.24.0 up
# sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
#
# sudo chmod +x /usr/local/bin/docker-compose
#
# docker run -itd -v /var/run/docker.sock:/var/run/docker.sock -v /root/test/:/var/tmp/ docker/compose:1.24.1  -f /var/tmp/docker-compose.yaml up -d

# docker-compose up






# FROM nginx
# COPY ./web/public /srv/www/static
# COPY ./default.conf /etc/nginx/conf.d/default.conf
# EXPOSE 8080
#
# FROM node:latest
# COPY ./web /src
# WORKDIR /src
# RUN npm install --production
# EXPOSE 3000
# CMD npm start
#
# FROM mongo
# EXPOSE 27017
