FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run sync
RUN npm run build

EXPOSE 3000

CMD ["node", "build/index.js"]
