import os
import time
import requests

def download_file(url, save_dir, session, filename=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if filename is None:
        filename = os.path.basename(url)

    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0" }
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        file_path = os.path.join(save_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"文件已成功下载并保存到: {file_path}")
    else:
        print(f"下载失败，状态码: {response.status_code}")


days = [i for i in range(1, 32)]
hours = [i for i in range(0, 24)]
session = requests.Session()
for day in days:
    for hour in hours:
        url = f"https://download.gatedata.org/futures_usdt/orderbooks_slice/202408/BTC_USDT-202408{day:02d}{hour:02d}.gz"
        print(f"Downloading day {day} hour {hour}: {url}")
        save_dir = './gate/lobsli'
        download_file(url, save_dir, session)
        time.sleep(1)
