FROM node:20-slim

WORKDIR /app

COPY package.json ./
RUN npm install --omit=dev

COPY . .

ENV PORT=3030
EXPOSE 3030

CMD ["node", "app.js"]
