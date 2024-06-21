#!/usr/bin/sh

echo "Starting cert-renewer initialization script"

for script in /scripts/*.sh; do
    echo "Running script: $script"
    sh "$script"
done


sendReloadSignal() {
    echo "Sending reload signal to proxy"
    curl proxy:1234/reload &> /dev/null
}

trap sendReloadSignal SIGHUP
trap "echo 'Stopping cert-renewer'; exit" SIGINT SIGTERM

while true; do
    killall sleep
    sleep 3600 &
    wait
done
