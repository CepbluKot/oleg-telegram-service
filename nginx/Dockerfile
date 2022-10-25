FROM nginx:1.20-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY olegbackend.crt /etc/ssl/olegbackend.crt
COPY olegbackend.key /etc/ssl/olegbackend.key
COPY ca.crt /etc/ssl/ca.crt

RUN mkdir -p /home/oleg/default
