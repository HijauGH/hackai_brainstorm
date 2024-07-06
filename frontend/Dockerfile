FROM node:16-alpine as builder
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build


FROM nginx:1.17.1-alpine
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY start-nginx.sh /start-nginx.sh
RUN chmod +x /start-nginx.sh
COPY --from=builder /usr/src/app/dist/client /usr/share/nginx/html
CMD ["/start-nginx.sh"]