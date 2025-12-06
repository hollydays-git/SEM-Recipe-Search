# syntax=docker/dockerfile:1
ARG NODE_VERSION=24.11.0

# Stage 1 — сборка фронта
FROM node:${NODE_VERSION}-alpine AS build
WORKDIR /usr/src/app

# Копируем package.json для установки зависимостей
COPY package*.json ./
RUN npm install

# Копируем весь код фронта
COPY . .
RUN npm run build

# Stage 2 — раздача prod билдов
FROM node:${NODE_VERSION}-alpine AS runtime
WORKDIR /usr/src/app
RUN npm install -g serve
COPY --from=build /usr/src/app/dist ./dist
EXPOSE 5173
CMD ["serve", "-s", "dist", "-l", "5173"]
