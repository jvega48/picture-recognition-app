# syntax=docker/dockerfile:1
# Use official node image as the base image
FROM node:latest as build

# set working directory
WORKDIR /web

# add `/app/node_modules/.bin` to $PATH
ENV PATH ./node_modules/.bin:$PATH

# install and cache app dependencies
COPY . ./
RUN npm run build

FROM nginx:1.17-alpine
RUN apk --no-cache add curl
RUN curl -L https://github.com/a8m/envsubst/releases/download/v1.1.0/envsubst-`uname -s`-`uname -m` -o envsubst && \
    chmod +x envsubst && \
    mv envsubst /usr/local/bin
COPY ./nginx.config /etc/nginx/nginx.template
CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/nginx.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
COPY --from=builder /opt/web/build /usr/share/nginx/html
FROM python:3.8-slim-buster

COPY requirements.txt .
RUN pip3 install --no-cache-dir requirements.txt

WORKDIR /app
COPY . /app 

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
