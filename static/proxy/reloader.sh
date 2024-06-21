reloader() {
    echo "Starting Reloader"

    tail -f  /var/log/nginx/reload.log | while read line; do
        echo "Reloading Nginx"
        nginx -s reload
    done    
}

echo "Launch Reloader"

touch  /var/log/nginx/reload.log

reloader &