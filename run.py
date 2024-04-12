import json
import logging
from asyncio import run
from source import XHS
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_url_path='/')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
app.config['TRUSTED_PROXIES'] = ['8.134.204.10']
limiter = Limiter(get_remote_address, app=app, default_limits=["100/day", "50/hour"])
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


async def main(link):
    try:
        work_path = ""
        folder_name = "Download"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        cookie = ""
        proxy = None
        timeout = 5
        chunk = 1024 * 1024 * 10
        max_retry = 5
        record_data = False  # 是否保存作品数据至文件
        image_format = "PNG"
        folder_mode = False  # 是否将每个作品的文件储存至单独的文件夹

        async with XHS(work_path=work_path,
                       folder_name=folder_name,
                       user_agent=user_agent,
                       cookie=cookie,
                       proxy=proxy,
                       timeout=timeout,
                       chunk=chunk,
                       max_retry=max_retry,
                       record_data=record_data,
                       image_format=image_format,
                       folder_mode=folder_mode,
                       ) as xhs:
            download = False
            str_result = await xhs.extract(link, download)
            json_data = json.loads(json.dumps(str_result, ensure_ascii=False))
            download_url = json_data[0]['下载地址'].split(' ')
            return download_url

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return str(e)


@app.route('/')
@limiter.limit("1/second", override_defaults=False)
def index():
    return app.send_static_file('index.html')


@app.route('/download', methods=['POST'])
@limiter.limit("10/day", override_defaults=False)
def get_download_url():
    link = request.json.get('imageUrl')
    download_url = run(main(link))
    if isinstance(download_url, str):
        logging.error(f"An error occurred: {download_url}")
        return jsonify({'error': download_url}), 500
    logging.info("Download URL retrieved successfully.")
    return jsonify({'downloadUrl': download_url})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
