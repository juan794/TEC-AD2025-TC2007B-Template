# build stage
FROM node:18 as build-stage
USER root
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 3080
CMD ["npm", "run", "dev"]