FROM nginx:1.20-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY ../crt/olegbackend.crt /etc/ssl/olegbackend.crt
COPY ../crt/olegbackend.key /etc/ssl/olegbackend.key
COPY ../crt/ca.crt /etc/ssl/ca.crt

RUN mkdir -p /home/oleg/default
