# -*- coding: UTF-8 -*-
# Title: convert
# Time: 06/03/2018 4:45 PM
# Author: cijian
# Email: cijianzy@gmail.com

import sources.convert_test as convert_test
import sources.convert_line as convert_line
import re
import os
import sources.utility as utility

os.system('rm ../output/output.m')
file_name = '/Users/cijian/workspace/EMAS/EMAS/SSH/ALYSSHSettingVC.swift'


out_put_h = '../output/output.h'
out_put_m = '../output/output.m'

lines = convert_test.get_clean_file(file_name)

def get_closure_lines(lines, start_line_number):
    bracket_count = 0;
    for p_line in range(start_line_number, len(lines)):
        line = lines[p_line]
        # simplely count closure bracket count to find lines belong same closure
        bracket_count = bracket_count + len(line.split('{')) - len(line.split('}'))
        if bracket_count == 0:
            return lines[start_line_number:p_line + 1]


def solve_class_lines(lines, deep):
    solve_lines(lines[1:-1], 'class', deep + 1)

def solve_func_lines(lines, deep):
    solve_lines(lines[1:-1], 'func', deep + 1)

def solve_lazy_var_lines(lines, deep):
    # pick lazy var define
    lazy_var_type = re.search('lazy var .*: *(.+?) =', lines[0]).group(1)
    lazy_var_name = re.search('lazy var (.+?):', lines[0]).group(1)
    utility.append_to_header('@property (nonatomic, strong) ' + lazy_var_type + ' *' + lazy_var_name + ';', 0)
    utility.append_to_body('-({} *){} '.format(lazy_var_type, lazy_var_name), 0)
    solve_lines(lines[1:-1], 'lazy_var', 1)
    utility.append_to_body('}', 0)
    utility.append_to_body('', 0)

def solve_if_lines(lines, deep):
    solve_lines(lines[1:-1], 'if', deep + 1)

def solve_line(line, deep):
    convert_line.solve_line(line, deep)

def solve_lines(lines, last_type, deep = 0):
    p_line = 0
    while p_line < len(lines):
        line = lines[p_line]
        if line.find('class') != -1:
            class_lines = get_closure_lines(lines, p_line)
            solve_class_lines(class_lines, deep)
            p_line = p_line + len(class_lines)
        elif line.find('func') != -1:
            func_lines = get_closure_lines(lines, p_line)
            solve_func_lines(func_lines, deep)
            p_line = p_line + len(func_lines)
        elif line.find('lazy var') != -1:
            lazy_var_lines = get_closure_lines(lines, p_line)
            solve_lazy_var_lines(lazy_var_lines, deep)
            p_line = p_line + len(lazy_var_lines)
        elif line.find('if ') != -1:
            if_lines = get_closure_lines(lines, p_line)
            solve_if_lines(if_lines, deep)
            p_line = p_line + len(if_lines)
        else:
            solve_line(line, deep)
            p_line = p_line + 1

solve_lines(lines, 'file', 0)