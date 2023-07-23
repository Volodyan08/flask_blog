# Use the official MySQL 8.0.33 image from Docker Hub
FROM mysql:8.0.33

# Set the environment variables for the MySQL database
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

# Expose port 3306 to allow external connections
EXPOSE 3306
