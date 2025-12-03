FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD [ "echo Hello World" ]
#CMD ["npm", "start"]

