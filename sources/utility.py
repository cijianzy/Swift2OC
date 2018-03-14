# -*- coding: UTF-8 -*-
# Title: utility
# Time: 07/03/2018 5:02 PM
# Author: cijian
# Email: cijianzy@gmail.com

def append_to_header(line, deep):
    append_to_file(line, '../output/output.h', deep)
def append_to_body(line, deep):
    append_to_file(line, '../output/output.m', deep)

def append_to_file(line, file_name, deep):
    file = open(file_name,'a', encoding='utf-8');
    file.write('    ' * deep + line + '\n')
    file.close()