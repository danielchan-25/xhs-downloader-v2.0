# xhs-downloader

项目灵感来源：https://github.com/JoeanAmier/XHS-Downloader/tree/master

在此基础上进行二次开发，新增了 `Flask` 框架。能在网页上进行下载，能直接部署在服务器上使用。


## 使用方法

1. 安装环境
    ```shell
    pip install -r requirements.txt
    ```

2. 启动 API
   ```shell
   python run.py 
   ```

3. 访问 `http://localhost:5000`
4. 输入小红书的分享链接，点击 "Get Download URL"， 即可获得下载地址。