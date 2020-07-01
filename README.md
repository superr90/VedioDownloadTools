### 完成状态

仅支持 Google Drive（包括 Google Docs，但不包括文件夹）文件、YouTube 视频下载。

程序仅获取文件的下载直链，下载部分交由 aria2 进行。

#### 待完善

* 支持 Google Drive 文件夹下载
* Google Drive 可能会有下载限制，最好使用 Google Drive API 获取直链

### 使用

#### Step1

``` bash
~ pip3 install -r requirements.txt
```

#### Step2

安装并配置 aria2 并开启 RPC。

#### Step3

修改 `main.py` 配置项，具体参考注视。

#### Step4

``` bash
~ python3 main.py
```
