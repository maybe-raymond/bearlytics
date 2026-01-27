#!/bin/bash
set -e

export USER=bear
CONTAINER_UID=${UID:-1000}
CONTAINER_GID=${GID:-1000}
groupmod -o -g "$CONTAINER_GID" $USER
usermod -o -u "$CONTAINER_UID" $USER
chown -R $USER:$USER /app

# Execute the command as the bear user
# If a single script argument, execute it directly; otherwise join arguments
if [ $# -eq 1 ]; then
    exec su $USER -c "$1"
else
    exec su $USER -c "$*"
fi

