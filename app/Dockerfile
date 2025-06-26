# Stage 1: Build the Vue.js application
FROM node:lts-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (if exists)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vue.js frontend for production
RUN npm run build

# Stage 2: Serve the built frontend with Nginx
FROM nginx:alpine AS final

# Set working directory (optional, but good practice)
WORKDIR /app

# Copy the built frontend from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the frontend
EXPOSE 80

# Command to start nginx
CMD ["nginx", "-g", "daemon off;"]
