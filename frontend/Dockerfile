# ════════════════════════════════
# STAGE 1 — BUILD
# Use Node.js to build React app
# ════════════════════════════════
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files first
# This caches node_modules if packages haven't changed
COPY frontend/package*.json ./

# Install all npm packages
RUN npm install

# Copy all frontend source code
COPY frontend/ .

# Build React app for production
# Creates a /build folder with static files
RUN npm run build

# ════════════════════════════════
# STAGE 2 — SERVE
# Use Nginx to serve the built files
# Much lighter than running Node.js
# ════════════════════════════════
FROM nginx:alpine

# Copy built files from Stage 1
# into Nginx's serving directory
COPY --from=build /app/build /usr/share/nginx/html

# Tell Docker this app uses port 80
EXPOSE 80

# Nginx starts automatically — no CMD needed