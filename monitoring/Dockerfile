FROM prom/prometheus

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY web.yml /etc/prometheus/web.yml

COPY entrypoint.sh /etc/entrypoint.sh

USER root
RUN chmod +x /etc/entrypoint.sh

ENTRYPOINT ["/etc/entrypoint.sh"]

CMD [ "--config.file=/etc/prometheus/prometheus.yml", "--web.config.file=/etc/prometheus/web.yml"]