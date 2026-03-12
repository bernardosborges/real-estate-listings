#!/bin/sh
set -e

# Path to store Godaddy credentials inside the container
CRED_FILE="/etc/letsencrypt/godaddy.ini"

# Create credentials file from environment variables
echo "Creating Godaddy credentials file..."
cat > "$CRED_FILE" <<EOF
dns_godaddy_key = ${GODADDY_API_KEY}
dns_godaddy_secret = ${GODADDY_SECRET_KEY}
EOF

# Set strict permissions so only root (the container) can read it
chmod 600 "$CRED_FILE"

# Run Certbot
echo "Starting Certbot to issue/renew certificates..."
args=""
for domain in $(echo "$DOMAINS" | tr ',' ' '); do
    args="$args -d $domain"
done

certbot certonly \
    --agree-tos \
    --email "${CERTBOT_EMAIL}" \
    --authenticator dns-godaddy \
    --dns-godaddy-credentials "$CRED_FILE" \
    --dns-godaddy-propagation-seconds 60 \
    --keep-until-expiring \
    --non-interactive \
    --expand \
    $args

echo "Certbot finished. Certificates are stored in /etc/letsencrypt"
exec "$@"
