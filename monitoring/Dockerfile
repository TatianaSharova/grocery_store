FROM prom/prometheus

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY web.yml /etc/prometheus/web.yml
CMD [ "--config.file=/etc/prometheus/prometheus.yml", "--web.config.file=/etc/prometheus/web.yml"]