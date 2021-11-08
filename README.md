# vikacg-checkin

基于 systemd/docker 的维咔 VikACG 自动签到

代码来自 [CrossingLK/vikacg-auto-check](https://github.com/CrossingLK/vikacg-auto-check)，此 repo 暂时只是将 scheduler 由 GitHub Actions 换为了 systemd/Docker，防止在 GitHub Actions 严查大潮下因签到型任务被 GitHub 封号（能解，但比较麻烦）

## 部署

TODO

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
