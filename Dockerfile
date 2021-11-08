FROM alpine:3

RUN apk add --no-cache tzdata
ENV TZ=Asia/Shanghai

COPY vikacg-checkin /bin/vikacg-checkin
COPY crontab.txt /etc/crontab
RUN crontab /etc/crontab

ENTRYPOINT ["crond", "-f", "-l", "2"]
