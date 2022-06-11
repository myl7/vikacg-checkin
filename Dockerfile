FROM python:3.10-alpine3.16
WORKDIR /app

RUN apk add --no-cache tzdata
ENV TZ=Asia/Shanghai

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py /usr/bin/vikacg-checkin

COPY crontab.txt /etc/crontab
RUN crontab /etc/crontab

ENTRYPOINT ["crond", "-f", "-l", "2"]
VOLUME [ "/var/log/vikacg-checkin.log" ]
