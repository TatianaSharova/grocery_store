#!/bin/sh

for i in $(env); do
    # Из env. берем все переменные, начинающиеся с PROMETHEUS_
    if echo "$i" | grep -q "^PROMETHEUS_"; then
        KEY=$(echo "$i" | sed "s/^PROMETHEUS_\([A-Z_]*\)=.*/\1/")
        VALUE=$(echo "$i" | sed "s/^PROMETHEUS_\([A-Z_]*\)=\(.*\)/\2/")

        # Заменяем переменные в файле prometheus.yml на значения из .env
        sed -i "s|PROMETHEUS_${KEY}|${VALUE}|g" /etc/prometheus/prometheus.yml

        # Заменяем переменные в файле web.yml на значения из .env
        sed -i "s|PROMETHEUS_${KEY}|${VALUE}|g" /etc/prometheus/web.yml
    fi
done

# Создаем диреректорию /prometheus/certs/, если она еще не создана
mkdir -p /prometheus/certs/

# Запуск Prometheus
exec /bin/prometheus "$@"
