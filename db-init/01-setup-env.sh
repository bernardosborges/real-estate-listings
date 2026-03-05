#!/bin/bash
set -e

# Create a temporary folder inside container
TEMPLATE_DIR="/db-templates"
INIT_DIR="/docker-entrypoint-initdb.d"

# Files
TEMPLATE_SQL="$TEMPLATE_DIR/02-create-db-template.sql"
FINAL_SQL="$INIT_DIR/02-create-db.sql"

# Substitute env variables
#envsubst < "$TEMPLATE_SQL" > "$FINAL_SQL"
#echo "✅ SQL final created in $FINAL_SQL"
