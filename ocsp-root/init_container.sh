if [ ! -f /etc/ocsp/index.txt.attr ] ; then
    echo "unique_subject=no" > /etc/ocsp/index.txt.attr
fi

/usr/bin/openssl ocsp \
    -index /etc/ocsp/index.txt \
    -port 80 \
    -rsigner /etc/ocsp/ocsp.crt \
    -rkey /etc/ocsp/ocsp.key \
    -CA /etc/ocsp/ca.crt \
    -multi 4 \
    -timeout 3600 \
    -ignore_err

exec crond -f