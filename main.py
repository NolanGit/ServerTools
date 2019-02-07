# coding=utf-8

#################################
#           此文件废弃           #
#  具体功能请分别见文件夹内主程序  #
#################################


import os
import sys
import traceback
import threading
from multiprocessing import Process


def get_all_files(dir_path):
    # 遍历dir_path下所有文件，包括子目录
    try:
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                yield file_path
            else:
                for i in get_all_files(file_path):
                    yield i
    except Exception:
        traceback.print_exc()


def get_program_path():
    str = sys._getframe().f_code.co_filename
    print(str)
    list = str.split('\\')
    final_path = ''
    for y in range(len(list) - 1):
        if y == 0:
            final_path = list[0]
        else:
            final_path = final_path + '\\' + list[y]
    all_file_path = get_all_files(final_path)
    final_program_path = []
    for single_file_path in all_file_path:
        if ".git" in single_file_path or "main.py" in single_file_path or 'dependent'in single_file_path:
            pass
        elif "py" not in single_file_path:
            pass
        else:
            final_program_path.append(single_file_path)
    return final_program_path


def start_programs(file_path):

    def program_to_command(file_path):
        with open(file_path, 'r') as f:
            exec(f.read())

    program_path, program = formart_file_path(file_path)
    program_to_command(file_path)

    # Process(target=)
final_program_path = get_program_path()
print(final_program_path)
for single_final_program_path in final_program_path:
    start_programs(single_final_program_path)
