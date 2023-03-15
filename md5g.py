"""
    author: wangshuo
    time: 2022/09/04 01:24
    version: 0.0.1

    md5g.py (md5 generate)
    校验文件生成工具 - 读取文件列表，生成一个 json 文件，存储文件的 md5 等相关信息，配合 md5v.py 来一键判断文件在拷贝（本地<->本地，本地<->远程）过程中，文件是否发生变化

"""

import json
import logging

from common import list_all_files, md5sum, argv

output_filename = 'md5sum.json'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%d/%m %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def dir_md5_json(root_dir):
    import time
    logging.info("[1] 开始获取文件列表")
    all_files = list_all_files(root_dir)
    logging.info('    文件列表读取完成，开始计算 md5 值')
    logging.info("[2] 开始计算MD5值")
    json_list = []
    for file in all_files:
        time_start = time.time()  # 记录开始时间
        md5_value = md5sum(file)
        time_end = time.time()  # 记录结束时间
        logging.info('    md5 计算完成，耗时 {:6.3f} 秒, 文件 {} '.format(float(time_end - time_start), file))
        obj = {
            "filepath": file.replace("\\","/"), # 文件路径 相对路径
            "md5sum": md5_value
        }
        json_list.append(obj)
    logging.info('    一共读取了 {} 个文件'.format(len(all_files)))
    return json_list

def main():
    root_dir = argv(logging)
    logging.info("起始目录为:" + root_dir)
    dir_json = dir_md5_json(root_dir)
    f = open(output_filename, 'w', encoding='utf-8')
    f.write(json.dumps(dir_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    f.flush()
    f.close()

if __name__ == '__main__':
    import time
    time_start = time.time()  # 记录开始时间
    logging.info("程序开始运行")
    main()
    time_end = time.time()  # 记录结束时间
    # 计算的时间差为程序的执行时间，单位为秒/s
    logging.info('程序结束运行，总耗时 {} 秒'.format(str(time_end - time_start)))