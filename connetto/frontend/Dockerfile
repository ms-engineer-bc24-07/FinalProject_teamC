FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

RUN npm install --save-dev prettier eslint eslint-config-prettier eslint-plugin-prettier

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
