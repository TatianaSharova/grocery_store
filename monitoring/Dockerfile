FROM prom/prometheus

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY web.yml /etc/prometheus/web.yml

COPY entrypoint.sh /etc/entrypoint.sh

USER root
RUN chmod +x /etc/entrypoint.sh

USER nobody

ENTRYPOINT ["/etc/entrypoint.sh"]