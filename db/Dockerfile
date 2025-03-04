FROM postgres:16

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /var/lib/postgresql/data && mkdir -p /docker-entrypoint-initdb.d

COPY data /var/lib/postgresql/data
COPY init /docker-entrypoint-initdb.d

RUN chown -R postgres:postgres /var/lib/postgresql/data /docker-entrypoint-initdb.d

USER postgres

EXPOSE 5432

CMD ["postgres"]
