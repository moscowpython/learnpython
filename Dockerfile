FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && apt-get upgrade -qq && \
    apt-get install -y --no-install-recommends \
    nginx \
    supervisor && \
    BUILD_DEPS='build-essential python3-dev git' && \
    apt-get install -y --no-install-recommends ${BUILD_DEPS} && \
    pip3 install -U pip setuptools && \
    pip3 install -U uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/ /etc/

ADD requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

COPY landing_page /opt/app

WORKDIR /opt/app
RUN mkdir -p /opt/staticfiles
RUN python3 manage.py collectstatic --noinput

RUN apt-get autoremove -y ${BUILD_DEPS} \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80
CMD ["supervisord", "-n"]