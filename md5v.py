"""
    author: wangshuo
    time: 2022/09/04 01:24
    version: 0.0.1

    md5 验证工具  (md5 verify)
    根据生成的 md5g.py 生成的 json 文件，进行对比

    # 流程
    # 1. 移除两个数组相同的元素，并输出信息
    # 2. 移除两个数组元素具有文件名称相同，但是md5值相同的元素，并输出信息
    # 3. 剩下的元素输出信息
        
"""
import json
import logging

import md5g
from common import argv

output_filename = 'md5sum.json'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%d/%m %H:%M:%S %p"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def main():
    import platform
    system = platform.system()

    root_dir = argv(logging)
    f = open(output_filename, 'rb+')
    dir_files1 = md5g.dir_md5_json(root_dir)
    dir_files2 = []
    for ele in json.loads(f.read().decode('utf-8')):
        new_ele = {
            "filepath": ele["filepath"], # 文件路径 相对路径
            "md5sum": ele["md5sum"]
        }
        if system == "Darwin" or system == "Linux":
            pass
        elif system == "Windows":
            new_ele["filepath"].replace("/","\\")
        dir_files2.append(new_ele)
    logging.info("[3] 开始对比，生成报告")
    dir_files_bigger = []
    dir_files_smaller = []
    if len(dir_files2) > len(dir_files1):
        dir_files_bigger = dir_files2.copy()
        dir_files_smaller = dir_files1.copy()
    else:
        dir_files_bigger = dir_files1.copy()
        dir_files_smaller = dir_files2.copy()

    for ele in dir_files_smaller:
        if ele in dir_files_bigger and ele in dir_files_smaller:
            dir_files1.remove(ele)
            dir_files2.remove(ele)
            logging.info('    校验完成，文件正常, md5： {:30}, 文件路径：{} '.format(ele['md5sum'], ele["filepath"]))

    dir_files3 = dir_files1.copy()
    dir_files4 = dir_files2.copy()
    for ele1 in dir_files3:
        for ele2 in dir_files4:
            if ele1["filepath"] == ele2["filepath"] and ele1["md5sum"] != ele2["md5sum"]:
                dir_files1.remove(ele1)
                dir_files2.remove(ele2)
                logging.error('    校验完成，文件被篡改 {} <-> {}, {}'.format(ele1["md5sum"], ele1["md5sum"], ele1["filepath"]))
                break
    for ele in dir_files1:
        logging.error("    新的地方有新的文件，{}".format(ele["filepath"]))
    for ele in dir_files2:
        logging.error("    文件在新的地方不存在，{}".format(ele["filepath"]))

if __name__ == '__main__':
    f = open(output_filename, 'rb+')
    import time
    time_start = time.time()  # 记录开始时间
    logging.info("程序开始运行")
    main()
    time_end = time.time()    # 记录结束时间
    logging.info('程序结束运行，总耗时 {} 秒'.format(str(time_end - time_start)))