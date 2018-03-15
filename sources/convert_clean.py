# -*- coding: UTF-8 -*-
# Title: convert_test
# Time: 06/03/2018 4:53 PM
# Author: cijian
# Email: cijianzy@gmail.com


# print(file_lines)

def get_clean_file(file_name):
    # file = open('/Users/cijian/workspace/EMAS/EMAS/SSH/ALYSSHSettingVC.swift', 'r')
    file = open(file_name, 'r',encoding="utf-8")
    file_lines = file.readlines()
    clean_lines = []
    for line in file_lines:
        line_splited = line.split('//')
        line = line_splited[0]
        if not line.strip():
            continue

        line = line.strip()
        line = line.replace("\n", '')
        clean_lines.append(line)
    return clean_lines


