"""
    author: wangshuo
    time: 2022/09/04 01:24
    version: 0.0.1

    md5g.py (md5 generate)
    校验文件生成工具 - 读取文件列表，生成一个 json 文件，存储文件的 md5 等相关信息，配合 md5v.py 来一键判断文件在拷贝（本地<->本地，本地<->远程）过程中，文件是否发生变化

"""

import json
import os
import logging
import time

output_filename = 'md5sum.json'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%d/%m %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def md5sum(path):
    import hashlib
    d5 = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(2024)
            if not data:
                break
            d5.update(data)  # update添加时会进行计算
    return d5.hexdigest()

def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
               if path.endswith('.pdf'):
                    _files.append(path)
    return _files

rootdir = r'D:\my-Linux\note-repository\note\PDF\backup'
json_list = []

def main():
    all_files = list_all_files(rootdir)
    logging.info('文件列表读取完成，开始计算 md5 值')
    for i in all_files:
        time_start = time.time()  # 记录开始时间
        md5_value = md5sum(i)
        time_end = time.time()  # 记录结束时间
        logging.info('md5 计算完成，耗时 {:6.3f} 秒, 文件 {} '.format(float(time_end - time_start), i))
        obj = {
            # 文件路径 相对路径
            "filepath": i.replace(rootdir, '').replace('\\', '/')[1:],
            "md5sum": md5_value
        }
        json_list.append(obj)
    f = open(output_filename, 'w', encoding='utf-8')
    f.write(json.dumps(json_list, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    f.flush()
    f.close()
    logging.info('一共读取了 {} 个文件'.format(len(all_files)))

if __name__ == '__main__':
    time_start = time.time()  # 记录开始时间
    logging.info("程序开始运行")
    main()
    time_end = time.time()  # 记录结束时间
    # 计算的时间差为程序的执行时间，单位为秒/s
    logging.info('程序结束运行，总耗时 {} 秒'.format(str(time_end - time_start)))