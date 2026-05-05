# Build stage
FROM node:lts-alpine AS builder
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Run stage — serve the compiled static files
FROM node:lts-alpine
RUN npm install -g serve
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/dist ./dist
EXPOSE 3000
USER node
CMD ["serve", "-s", "dist", "-l", "3000"]
