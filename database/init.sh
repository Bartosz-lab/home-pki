#!/usr/bin/env bash

echo "Starting database initialization script"

for script in /docker-entrypoint-initdb.d/*.sh; do
    echo "Running script: $script"
    sh "$script"
done