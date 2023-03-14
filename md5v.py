"""
    author: wangshuo
    time: 2022/09/04 01:24
    version: 0.0.1

    md5 验证工具  (md5 verify)
    根据生成的 md5g.py 生成的 json 文件，进行对比

"""
import json
import os
import logging

from common import md5sum, argv

output_filename = 'md5sum.json'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%d/%m %H:%M:%S %p"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def main():
    import platform
    system = platform.system()

    root_dir = argv(logging)
    f = open(output_filename, 'rb+')
    for obj in json.loads(f.read().decode('utf-8')):
        filepath = root_dir + os.sep + obj['filepath']
        md5_value = ""
        if os.path.exists(filepath):
            if system == "Darwin" or system == "Linux":
                md5_value = md5sum(filepath)
            elif system == "Windows":
                md5_value = md5sum(filepath.replace("/","\\"))
        else:
            logging.error('文件不存在 {} '.format(filepath))
            continue
        if md5_value == obj['md5sum']:
            logging.info('校验完成，文件正常,md5： {:30}, 文件路径：{} '.format(obj['md5sum'], filepath))
        else:
            logging.error('校验完成，文件被篡改 {}'.format(filepath))
    f.close()

if __name__ == '__main__':
    import time
    time_start = time.time()  # 记录开始时间
    logging.info("程序开始运行")
    main()
    time_end = time.time()    # 记录结束时间
    logging.info('程序结束运行，总耗时 {} 秒'.format(str(time_end - time_start)))
