#!/bin/bash

# RUN sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common -y
RUN sudo apt-get install docker-ce docker-ce-cli containerd.io -y



# RUN chmod +x script.sh

# ENTRYPOINT ["sh", "script.sh"]




# docker run --rm -it -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock docker/compose:1.24.0 up
# sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
#
# sudo chmod +x /usr/local/bin/docker-compose
#
# docker run -itd -v /var/run/docker.sock:/var/run/docker.sock -v /root/test/:/var/tmp/ docker/compose:1.24.1  -f /var/tmp/docker-compose.yaml up -d

docker-compose up






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
