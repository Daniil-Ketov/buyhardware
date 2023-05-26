# Базовый образ для Node.js
FROM node:20-bullseye

# Создание и установка рабочей директории
WORKDIR /app

# Копирование зависимостей проекта
COPY package.json yarn.lock /app/

# Установка зависимостей
RUN yarn install --frozen-lockfile --production

# Копирование исходного кода
COPY . /app

# Запуск проекта
CMD ["yarn", "start"]