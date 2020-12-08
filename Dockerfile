FROM python:3.8-slim-buster as base

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

FROM base AS builder

RUN set -xe; \
    apt-get update && apt-get install -y \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
            build-essential\
            gcc\
            g++ \
            libc-dev \
            libffi-dev \
            libxml2-dev \
            libxslt-dev \
            libpq-dev \
            git \
            zlib1g-dev \
            libjpeg-dev \
            libmagic-dev \
            curl \
            wget \
            ca-certificates

ADD requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt


FROM base

RUN groupadd -g 800 -r unprivileged && useradd -r -g 800 -u 800 -m unprivileged

RUN set -xe; \
    apt-get update && apt-get install -y \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
        locales gosu procps; \
            gosu nobody true;

COPY --from=builder /install /usr/local

RUN pip install gunicorn==20.0.4

RUN echo "LC_ALL=ru_RU.UTF-8" >> /etc/environment && echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "LANG=ru_RU.UTF-8" > /etc/locale.conf && locale-gen ru_RU.UTF-8

COPY landing_page /opt/app
COPY entrypoint.sh /opt/app
COPY wait-for-it.sh /opt/app

RUN chmod +x /opt/app/entrypoint.sh
RUN chmod +x /opt/app/wait-for-it.sh

WORKDIR /opt/app
RUN mkdir -p /opt/app/static && mkdir -p /opt/staticfiles && python3 manage.py collectstatic --noinput

RUN chown -R unprivileged:unprivileged /opt/app

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8000

ENTRYPOINT ["/opt/app/entrypoint.sh"]
CMD ["runserver"]
