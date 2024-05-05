from os import mkdir
from os.path import exists, join
from urllib3 import request, PoolManager
from json import loads
from zipfile import ZipFile
from shutil import move

class Setup:
    def __init__(self) -> None:
        # Chrome webdriver setup
        self.webdriver_dir = 'C:\\webdriver'
        if exists(self.webdriver_dir) is False:
            mkdir(self.webdriver_dir)
        self.webdriver_path = join(self.webdriver_dir, 'chromedriver.exe')
        self.webdriver_download_path = join(self.webdriver_dir, 'chromedriver.zip')
        self.webdriver_version = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'

    def selenium(self) -> None:
        try:
            if exists(self.webdriver_path) is False:
                # Get the url of downloading webdriver
                download_url = [webdriver for webdriver in loads(request('GET', self.webdriver_version).data.decode())['channels']['Stable']['downloads']['chromedriver'] if webdriver['platform'] == 'win64'][0]['url']

                # Download webdriver
                pmanager = PoolManager()
                download = pmanager.request('GET', download_url)
                with open(self.webdriver_download_path, 'wb') as f:
                    f.write(download.data)

                # Unzip downloaded package for webdriver
                with ZipFile(self.webdriver_download_path, 'r') as zip:
                    zip.extractall(self.webdriver_dir)
                    for filename in zip.namelist():
                        move(join(self.webdriver_dir, filename), join(self.webdriver_dir, filename.split('/')[-1]))
        except:
            raise