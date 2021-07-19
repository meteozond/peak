FROM postgres:13.2

RUN apt-get update && apt-get install -y \
    # Geospatial libraries
    binutils libproj-dev gdal-bin \
    libgeos-dev \
    postgresql-13-postgis-3-scripts \
    postgis

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
