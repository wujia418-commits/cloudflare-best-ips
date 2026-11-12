# cloudflare-best-ips

Cloudflare 优选 IP 节点，每日自动测速更新。

> 注意：GitHub Actions 的测速机房在境外，测出的“最快”适合作为参考。
> 你在国内用的时候，建议从 `ips/best-ipv4.txt` 里挑前几个，在本地再测一次延迟，
> 选你自己网络下最快的那个。

## 每天更新什么

- `ips/cloudflare-ips-v4.txt`：Cloudflare 官方 IPv4 段，每天同步
- `ips/cloudflare-ips-v6.txt`：Cloudflare 官方 IPv6 段，每天同步
- `ips/best-ipv4.txt`：测速后排在前面的 IPv4，每天更新
- `ips/best-ipv4-with-port.txt`：上面那些 IP 加上常用端口的版本，方便直接填
- `result.csv`：最近一次完整测速结果，含延迟、下载速度

更新时间：每天北京时间 02:00 自动跑一次，也可以在 Actions 里点 Run workflow 手动跑。

## 怎么用

1. 打开 `ips/best-ipv4.txt`，复制一个 IP
2. 在你的 Cloudflare / 域名 / 客户端里，把它作为优选 IP 填进去
3. 如果一个 IP 变慢了，换列表里的下一个

## 本地自己测一次

如果你在自己电脑上想测：

```bash
# 下载 CloudflareSpeedTest 后，在仓库目录运行
./CloudflareST -f ips/cloudflare-ips-v4.txt -o result.csv
```

跑完看 `result.csv`，按延迟从低到高排，就是你本地的最优结果。

## 文件说明

- `.github/workflows/update-ips.yml`：每日自动更新的流程
- `scripts/parse_result.py`：把测速结果整理成优选列表
- `ips/`：所有 IP 列表都在这里
