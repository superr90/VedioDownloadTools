import requests
from sys import stdout

# 获取 Google Drive 下载直链
class GoogleDriveDownloader:
    CHUNK_SIZE = 32768
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

    @staticmethod
    def download_file_from_google_drive(file_id, proxies={}):
        session = requests.Session()

        stdout.flush()

        response = session.get(
            GoogleDriveDownloader.DOWNLOAD_URL,
            params={"id": file_id},
            stream=True,
            proxies=proxies,
        )

        token = GoogleDriveDownloader._get_confirm_token(response)
        if token:
            params = {"id": file_id, "confirm": token}
            response = session.get(
                GoogleDriveDownloader.DOWNLOAD_URL,
                params=params,
                stream=True,
                proxies=proxies,
            )

        # print(f"{GoogleDriveDownloader.DOWNLOAD_URL}&id={file_id}&confirm={token}")
        return f"{GoogleDriveDownloader.DOWNLOAD_URL}&id={file_id}&confirm={token}"

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    # 保存文件
    @staticmethod
    def _save_response_content(response, destination, showsize, current_size):
        with open(destination, "wb") as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    if showsize:
                        print(
                            "\r" + GoogleDriveDownloader.sizeof_fmt(current_size[0]),
                            end=" ",
                        )
                        stdout.flush()
                        current_size[0] += GoogleDriveDownloader.CHUNK_SIZE

    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "{:.1f} {}{}".format(num, unit, suffix)
            num /= 1024.0
        return "{:.1f} {}{}".format(num, "Yi", suffix)

