# vikacg-checkin

基于 systemd/Docker 的[维咔 VikACG](https://www.vikacg.com/) 自动签到

## 部署

首先获取 `Authorization` token：打开 [VikACG 签到界面](https://www.vikacg.com/mission/today)，按 F12 键打开浏览器控制台并切换到 Network 标签页，然后在浏览页面中签到一次，再在控制台页面中 Network 标签页内的网络流量列表中找到发往 `/wp-json/b2/v1/userMission` 的请求，然后复制右侧 Request Headers 中 authorization 字段的值即可，后续我们把此值记作 `<AUTH>`

然后从以下两种方案中选一种进行部署：

### Docker

首先安装好 Docker，然后获取并使用 `myl7/vikacg-checkin` 这个镜像：

```bash
docker pull myl7/vikacg-checkin
docker run -d \
  --name=vikacg-checkin \
  --restart=unless-stopped \
  -e AUTH=<AUTH>
  -v vikacg-checkin.log:/var/log/vikacg-checkin.log:ro \
  myl7/vikacg-checkin
```

Log 在容器内 /var/log/vikacg-checkin.log 中，可以 read-only mount 出来方便阅读

### systemd

首先 git clone 这个 repo，然后把各文件移至对应位置，并在 system level 安装需要的 Python 包：

```bash
git clone https://github.com/myl7/vikacg-checkin && cd vikacg-checkin
sudo mv run.py /usr/local/bin/vikacg-checkin
sudo mv vikacg-checkin.{service,timer} /etc/systemd/system
# 暂时只要 requests：
sudo pip3 install -r requirements.txt
# 或者
sudo apt install python3-requests
```

然后创建配置文件 `/etc/default/vikacg-checkin` 并写入配置，格式和 dotenv/env 的格式一样：

```bash
sudo touch /etc/default/vikacg-checkin
echo 'AUTH=<AUTH>' | sudo tee /etc/default/vikacg-checkin
```

最后启用这个 systemd 定时器：

```bash
sudo systemctl daemon-reload
sudo systemctl start vikacg-checkin.timer
sudo systemctl enable vikacg-checkin.timer
```

Log 可以通过 systemd 的 log 查询方式来查询：

```bash
sudo systemctl status vikacg-checkin.timer
sudo systemctl status vikacg-checkin.service
```

## 配置

|      |      |                                            |
| ---- | ---- | ------------------------------------------ |
| AUTH | 必需 | `Authorization` token，用于身份认证        |
| UA   | 可选 | User Agent，默认使用 `requests` 包的默认值 |

## 自定义

[`run.py`](run.py) 文件中留有成功 hook 和失败 hook，方便实现如出错后发送邮件进行通知等功能

以发送邮件为例，Python 发送邮件可以参考[这个的 Python 发送邮件实现](https://gist.github.com/myl7/95e94cf19388f182bd4194ecff7352d8)，将其中的代码填在需要的 hook 中即可

默认签到周期配置在 [`crontab.txt`](crontab.txt) 或 [`vikacg-checkin.timer`](vikacg-checkin.timer) 中，如需在部署后修改也可以通过修改容器中 `/etc/crontab` 并重载 crontab 或是修改 `/etc/systemd/system/vikacg-checkin.timer` 并重载 systemd 实现

特别地，受益于 systemd timer 的机制，systemd 部署的此应用将会在 3h 的时间段内的随机一个时刻进行签到

## 致谢

- [CrossingLK/vikacg-auto-check](https://github.com/CrossingLK/vikacg-auto-check)
  - `stale/go` 分支上的旧实现即基于其

## License

Copyright (c) 2022 myl7

SPDX-License-Identifier: Apache-2.0
