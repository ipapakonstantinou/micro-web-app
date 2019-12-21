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
