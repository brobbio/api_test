#!/bin/sh

echo "Waiting for DB..."
echo "Trying ${DB_HOST} ${DB_PORT}"

until python - <<EOF
import socket, sys
s = socket.socket()
try:
    s.settimeout(1)
    s.connect(("${DB_HOST}", int("${DB_PORT}")))
    s.close()
except Exception:
    sys.exit(1)
EOF
do
  sleep 1
done

echo "DB is up"

uvicorn main:app --host 0.0.0.0 --port 8000