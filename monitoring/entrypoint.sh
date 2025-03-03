#!/bin/sh

for i in $(env); do
    # Из env. берем все переменные, начинающиеся с PROMETHEUS_
    if echo "$i" | grep -q "^PROMETHEUS_"; then
        KEY=$(echo "$i" | sed "s/^PROMETHEUS_\([A-Z_]*\)=.*/\1/")
        VALUE=$(echo "$i" | sed "s/^PROMETHEUS_\([A-Z_]*\)=\(.*\)/\2/")

        # Заменяем переменную в файле prometheus.yml на значение из .env
        sed -i "s/PROMETHEUS_${KEY}/${VALUE}/g" /etc/prometheus/prometheus.yml
    fi
done

# Запуск Prometheus
exec /bin/prometheus "$@"