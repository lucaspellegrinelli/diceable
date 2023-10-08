FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install dotenv

COPY . .

RUN npm run sync
RUN npm run build

ENV PORT=3000
EXPOSE 3000

CMD ["node", "-r", "dotenv/config", "server.js"]