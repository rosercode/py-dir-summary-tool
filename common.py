import os

def list_all_files(root_dir):
    """获取目录下所有文件的路径"""
    file_paths = []
    for root, directories, files in os.walk(root_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def md5sum(path):
    """计算文件的MD5值"""
    import hashlib
    d5 = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(2024)
            if not data:
                break
            d5.update(data)  # update添加时会进行计算
    return d5.hexdigest()

def argv(logging):
    """获取起始路径"""
    import sys, os
    if len(sys.argv)!=2:
        logging.info("起始路径不存在，默认使用路径")
        root_dir = "."
    else:
        root_dir = sys.argv[1]
    if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
        logging.info("目录不存在，获取不是目录")
        sys.exit(0)
    return root_dir