#!/bin/bash

# Определяем путь к сертификатам на хосте
CERTS_PATH_=${CERTS_PATH}
CRT_FILE="server.crt"
KEY_FILE="server.key"

# Путь в контейнере
CONTAINER_NAME="store_prometheus"
DEST_PATH="prometheus/certs"

# Копируем файлы в контейнер
docker cp "$CERTS_PATH_/$CRT_FILE" "$CONTAINER_NAME:$DEST_PATH/"
docker cp "$CERTS_PATH_/$KEY_FILE" "$CONTAINER_NAME:$DEST_PATH/"

# Проверяем, скопировались ли файлы
if [ $? -eq 0 ]; then
    echo "Файлы успешно скопированы в контейнер $CONTAINER_NAME в $DEST_PATH"
else
    echo "Ошибка при копировании файлов"
fi