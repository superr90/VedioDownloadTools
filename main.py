import xlrd
import json
import pafy
import aria2p
import requests
from gdler import GoogleDriveDownloader as gdd

# 配置
FILEPATH = "./Content Review Sign-Up.xlsx"  # Excel 文件路径
TABLES = ["Week 1", "Week 2", "Week 3"]  # 需要下载的 Sheet
PROXIES = {"https": "http://127.0.0.1:1080/"}  # 代理
ARIA2 = {"host": "http://127.0.0.1", "port": 6800, "secret": ""}  # aria2 RPC 设置
OUT_DIR_ROOT = "/"  # 文件保存根目录（绝对路径）

r = {}
data = xlrd.open_workbook(FILEPATH)
aria2 = aria2p.API(aria2p.Client(**ARIA2))

# 格式化需要下载的文件目录
for name in TABLES:
    r[name] = {"GoogleDrive": {}, "YouTube": {}}
    table = data.sheet_by_name(name)
    for i in range(12, table.nrows):
        x = table.row_values(i)
        if (
            "drive.google.com" in x[1] or "docs.google.com" in x[1]
        ) and "folders" not in x[1]:
            r[name]["GoogleDrive"][x[0]] = x[1]
        elif "youtu.be" in x[1] or "youtube.com" in x[1]:
            r[name]["YouTube"][x[0]] = x[1]

# print(json.dumps(r))

# 获取下载直链并添加到 aria2
for name in TABLES:
    print(f"{name}")

    # Google Drive 部分
    print(f"# GoogleDrive")
    for t in r[name]["GoogleDrive"]:
        x = r[name]["GoogleDrive"][t]
        tmp = x.split("/d/")[1].split("/")[0]
        url = gdd.download_file_from_google_drive(file_id=tmp, proxies=PROXIES,)
        print(f"## Adding {t} to aria2...")
        aria2.add_uris([url], {"dir": f"{OUT_DIR_ROOT}/{name}"})

    # YouTube 部分
    print(f"# YouTube")
    for t in r[name]["YouTube"]:
        x = r[name]["YouTube"][t]
        video = pafy.new(x)
        best = video.getbest(preftype="mp4")
        print(f"## Adding {t} to aria2...")
        aria2.add_uris([best.url], {"dir": f"{OUT_DIR_ROOT}/{name}", "out": f"{t}.mp4"})

