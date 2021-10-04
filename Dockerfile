# syntax=docker/dockerfile:1
# Use official node image as the base image
# FROM node:latest as build

# set working directory
# WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
# COPY package.json package-lock.json /app/
# RUN cd /app && npm install
# RUN npm install -g @angular/cli

# add app
#COPY . /app

# start app
# RUN cd /app && npm run build

# FROM nginx:1.17.8
# RUN rm -rf /usr/share/nginx/html/*
# COPY nginx.conf /etc/nginx/nginx.conf
# COPY --from=build /app/dist/TheLibrary/ /usr/share/nginx/html/
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

FROM python:3.8-slim-buster

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app 

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
