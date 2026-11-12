#!/usr/bin/env python3
"""把 CloudflareSpeedTest 的 result.csv 整理成优选 IP 列表。

只读 result.csv，不做网络请求。没有结果文件时，不清空旧列表。
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(ROOT, "result.csv")
IPS_DIR = os.path.join(ROOT, "ips")

# CloudflareSpeedTest 的 CSV 表头一般是：IP 地址,已发送,已接收,丢包率,平均延迟,下载速度(MB/s)
# 不同版本表头可能略有不同，这里按位置和关键字兼容处理。
def find_col(fieldnames, keywords):
    for i, name in enumerate(fieldnames):
        for kw in keywords:
            if kw in name:
                return i
    return None

def main():
    if not os.path.exists(RESULT):
        print("result.csv not found, keeping old lists")
        return

    with open(RESULT, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) < 2:
        print("result.csv is empty, keeping old lists")
        return

    header = rows[0]
    ip_idx = find_col(header, ["IP"])
    loss_idx = find_col(header, ["丢包", "loss"])
    delay_idx = find_col(header, ["延迟", "平均延迟"])
    speed_idx = find_col(header, ["下载速度", "速度"])

    if ip_idx is None:
        ip_idx = 0

    candidates = []
    for r in rows[1:]:
        if len(r) <= ip_idx or not r[ip_idx].strip():
            continue
        ip = r[ip_idx].strip()
        try:
            loss = float(r[loss_idx].replace("%", "")) if loss_idx is not None and r[loss_idx] else 0.0
        except Exception:
            loss = 0.0
        try:
            delay = float(r[delay_idx]) if delay_idx is not None and r[delay_idx] else 9999.0
        except Exception:
            delay = 9999.0
        try:
            speed = float(r[speed_idx]) if speed_idx is not None and r[speed_idx] else 0.0
        except Exception:
            speed = 0.0
        # 丢包太高的不要
        if loss > 10:
            continue
        candidates.append((delay, -speed, ip))

    candidates.sort()
    top = [ip for _, _, ip in candidates[:20]]

    if not top:
        print("no usable candidates, keeping old lists")
        return

    os.makedirs(IPS_DIR, exist_ok=True)
    with open(os.path.join(IPS_DIR, "best-ipv4.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(top) + "\n")
    with open(os.path.join(IPS_DIR, "best-ipv4-with-port.txt"), "w", encoding="utf-8") as f:
        # 443 是最常用的端口，方便直接复制使用
        f.write("\n".join(f"{ip}:443" for ip in top) + "\n")

    print(f"wrote {len(top)} best IPs")

if __name__ == "__main__":
    main()
