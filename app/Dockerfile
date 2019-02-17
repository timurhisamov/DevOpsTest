FROM python:3.7.2-alpine3.9
ENV TZ=Europe/Moscow
WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache bash openssh supervisor && \
    ssh-keygen -A && \
    echo Port 2222 >> /etc/ssh/sshd_config && \
    mkdir -p /etc/supervisor.d && \
    pip install --no-cache-dir -r requirements.txt
COPY devkey.pub /root/.ssh/authorized_keys
COPY supervisord.conf /etc/supervisord.conf
EXPOSE 5000 2222
#CMD [ "python", "./service.py", "-conf", "./conf.yml" ]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]