import os


def list_all_files(root_dir):
    from os import walk
    all_files = []
    for (dir_path, dir_names, file_names) in walk(root_dir):
        a_list = []
        for file_name in file_names:
            a_list.append(dir_path + os.sep + file_name)
        print(dir_path, dir_names, file_names)
        all_files.extend(a_list)
    return all_files

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

def argv(logging):
    import sys, os
    if len(sys.argv)!=2:
        logging.info("起始路径不存在，默认使用路径")
        root_dir = ".\\"
    else:
        root_dir = sys.argv[1]
    if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
        logging.info("目录不存在，获取不是目录")
        sys.exit(0)
    return root_dir