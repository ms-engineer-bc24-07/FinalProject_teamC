FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

RUN npm install --save-dev prettier eslint eslint-config-prettier eslint-plugin-prettier


# CHOKIDAR_USEPOLLINGの環境変数を設定
ENV CHOKIDAR_USEPOLLING=true

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
