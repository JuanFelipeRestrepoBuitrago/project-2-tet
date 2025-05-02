# Use the official neilpang/acme.sh image as the base
FROM neilpang/acme.sh:latest

# Install docker-cli
RUN apk add --no-cache docker-cli

# Copy the reload_nginx.sh script
COPY reload_nginx.sh /reload_nginx.sh

# Ensure the script is executable
RUN chmod +x /reload_nginx.sh

# Set the default entrypoint to run acme.sh cron and keep the container alive
ENTRYPOINT ["/bin/sh", "-c", "acme.sh --cron --home /acme.sh; sleep infinity"]