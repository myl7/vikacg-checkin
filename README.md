# vikacg-checkin

基于 systemd/docker 的维咔 VikACG 自动签到

代码来自 [CrossingLK/vikacg-auto-check](https://github.com/CrossingLK/vikacg-auto-check)，此 repo 暂时只是将 scheduler 由 GitHub Actions 换为了 systemd/Docker，防止在 GitHub Actions 严查大潮下因签到型任务被 GitHub 封号（能解，但比较麻烦）

## 部署

首先获取 `AUTHORIZATION` 参数，具体方法参见此文档尾部原 README 的介绍

### Docker

```
docker run -d --restart=always --name=vikacg-checkin -e AUTHORIZATION=... myl7/vikacg-checkin
```

每天东八区 17:00 签到。
如需更改时间可以修改 `crontab.txt` 之后重新用 `build.sh` 和 `docker build` 构建自己的 Docker image。

### systemd

将构建好的 `vikacg-checkin`（可以自行使用 `build.sh` 构建或是从 [Release](https://github.com/myl7/vikacg-checkin/releases) 下载）放到 `/usr/local/bin/vikacg-checkin`；
然后将 `vikacg-checkin.service` 和 `vikacg-checkin.timer` 复制到 `/etc/systemd/system/`，并执行 `systemctl daemon-reload` 和 `systemctl enable vikacg-checkin.timer`。
受益于 systemd timer，每天会在东八区 17:00 之后 3h 内的某一随机时刻签到。
如不需要随机时间签到，将 `vikacg-checkin.timer` 中的 `RandomizedDelaySec=3h` 一行删除并执行 `systemctl daemon-reload` 和 `systemctl restart vikacg-checkin.timer` 即可。
如需更改时间可以修改 `vikacg-checkin.timer` 中的 `OnCalendar` 并同上重启即可。

## License

All modifications are still licensed under MIT

后续部分是原 repo 的 README：

---

# vikacg-auto-check

基于GitHub Action的维咔VikACG自动签到

## 使用说明

1、获取authorization

- 登录VikACG，浏览器F12打开控制台，点击签到，在控制台找到任一请求，复制Request Headers中的authorization的值

2、Fork本仓库，然后进入你fork好的仓库，依次选择Settings-Secrets-New repository secret

- 此时进入密匙创建选项，Name填`AUTHORIZATION`，Value填刚刚复制好的authorization，如有多个账户，需要用`#`隔开

3、点击项目上方的Actions选项

- 首次启用按照提示启用即可
- 发起一次push，例如点击打开`README.md`，点击右上方修改按钮（Edit this ile），在末尾添加一个空格，点击最下方的Propose changes按钮提交

## 查看签到记录

点击Actions-All workflows，如果已有`VikACG Auto Check In`，则已设置成功，点击可查看执行记录
