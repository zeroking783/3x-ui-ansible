FROM ubuntu:22.04

ENV TZ=Europe/Moscow

ARG VPN_PORT=64444
ARG VPN_USERNAME=admin123
ARG VPN_PASSWORD=password123
ARG VPN_WEB_BASE_PATH=mamamamamama

RUN apt-get update && apt-get install -y \
    bash \
    wget \
    fail2ban \
    systemctl \
    && rm -rf /var/lib/apt/lists/*

RUN rm -f /etc/fail2ban/jail.d/alpine-ssh.conf \
  && cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local \
  && sed -i "s/^\[ssh\]$/&\nenabled = false/" /etc/fail2ban/jail.local \
  && sed -i "s/^\[sshd\]$/&\nenabled = false/" /etc/fail2ban/jail.local \
  && sed -i "s/#allowipv6 = auto/allowipv6 = auto/g" /etc/fail2ban/fail2ban.conf

WORKDIR /app/3x-ui

RUN wget https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh

RUN bash install.sh

WORKDIR /usr/local/x-ui

RUN ./x-ui setting -port ${PORT} -username ${USERNAME} -password ${PASSWORD} -webBasePath ${WEBBASEPATH}

RUN ./x-ui restart

CMD ["/usr/local/x-ui/x-ui"]