# Use an official Nginx runtime as a parent image
FROM nginx:alpine

# Copy static assets to Nginx's default public directory
COPY index.html /usr/share/nginx/html/index.html

# (Optional) Copy a custom Nginx configuration if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 