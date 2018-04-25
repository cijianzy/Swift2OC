# -*- coding: UTF-8 -*-
# Title: convert
# Time: 06/03/2018 4:45 PM
# Author: cijian
# Email: cijianzy@gmail.com

import sources.convert_clean as convert_test
import sources.convert_line as convert_line
import re
import os
import sources.utility as utility

os.system('rm ../output/output.m')
os.system('rm ../output/output.h')
# file_name = '/Users/cijian/workspace/EMAS/EMAS/SSH/ALYSSHSettingVC.swift'
file_name = '../input/input.swift'

out_put_h = '../output/output.h'
out_put_m = '../output/output.m'

lines = convert_test.get_clean_file(file_name)

def get_closure_lines(lines, start_line_number):
    """
    splite closure between '{'  '}'

    :param lines: content
    :param start_line_number: should recognize begein this line
    :return: Null
    """

    bracket_count = 0;
    for p_line in range(start_line_number, len(lines)):
        line = lines[p_line]
        # simplely count closure bracket count to find lines belong same closure
        bracket_count = bracket_count + len(line.split('{')) - len(line.split('}'))
        if bracket_count == 0:
            return lines[start_line_number:p_line + 1]


def solve_class_lines(lines, deep):
    """
    Convert Objective-c class define sentence to Swift class
    :param lines: class closure
    :param deep: the deep to print
    """
    class_name = re.search('class (.+?):', lines[0]).group(1)
    if class_name == None:
        class_name = re.search('class (.+?)', lines[0]).group(1)
    utility.append_to_body('@implementation {}'.format(class_name), 0)
    utility.append_to_header('@interface {}'.format(class_name), 0)
    solve_lines(lines[1:-1], 'class', 1)
    utility.append_to_body('@end', 0)
    utility.append_to_body('', 0)
    utility.append_to_header('@end', 0)
    utility.append_to_header('', 0)

def solve_protocol_lines(lines, deep):
    pass


def solve_func_lines(lines, deep):

    no_point_type = {'Int': 'Int'}
    m = re.search('> *(.+?) *{', lines[0])

    """Get func return type"""
    if m:
        func_return_type = m.group(1)

        if func_return_type not in no_point_type.keys():
            func_return_type += ' *'
    else:
        func_return_type = 'void'

    utility.append_to_body('-({}){} '.format(func_return_type,lines[0]) + '{', 0)
    solve_lines(lines[1:-1], 'func', 1)
    utility.append_to_body('}', 0)
    utility.append_to_body('', 0)

def solve_lazy_var_lines(lines, deep):
    # pick lazy var define
    lazy_var_type = re.search('lazy var .*: *(.+?) =', lines[0]).group(1)
    lazy_var_name = re.search('lazy var (.+?):', lines[0]).group(1)
    utility.append_to_header('@property (nonatomic, strong) ' + lazy_var_type + ' *' + lazy_var_name + ';', 0)
    utility.append_to_body('@synthesize {} = _{};'.format(lazy_var_name, lazy_var_name), 0)
    utility.append_to_body('-({} *){} '.format(lazy_var_type, lazy_var_name) + '{', 0)
    utility.append_to_body('if(!_' + lazy_var_name + ') {', 1)
    solve_lines(lines[1:-1], 'lazy_var', 2)
    utility.append_to_body('}', 1)
    utility.append_to_body('return _{};'.format(lazy_var_name), 1)
    utility.append_to_body('}', 0)
    utility.append_to_body('', 0)

def solve_if_lines(lines, deep):
    solve_lines(lines[1:-1], 'if', deep + 1)

def solve_line(line, deep):
    convert_line.solve_line(line, deep)

def solve_snp_layout(lines, deep):
    snp_property = re.search(' *(.+?).snp', lines[0]).group(1)
    utility.append_to_body('[' + snp_property + ' mas_makeConstraints:^(MASConstraintMaker *make) {', deep)
    solve_lines(lines[1:-1], 'snp', deep + 1)
    utility.append_to_body('}', deep)
    utility.append_to_body('', deep)

def solve_lines(lines, last_type, deep = 0):

    p_line = 0
    while p_line < len(lines):
        line = lines[p_line]
        if line.find('protocol'):
            protocol_lines = get_closure_lines(lines, p_line)
            p_line = p_line + len(protocol_lines)
        if line.find('class ') != -1:
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
        elif line.find('if ') != -1 or line.find('else if') != -1:
            if_lines = get_closure_lines(lines, p_line)
            solve_if_lines(if_lines, deep)
            p_line = p_line + len(if_lines)
        elif line.find('makeConstraints') != -1:
            snp_lines = get_closure_lines(lines, p_line)
            solve_snp_layout(snp_lines, deep)
            p_line = p_line + len(snp_lines)
        elif line.find(') {') != -1:
            func_call_with_block_lines = get_closure_lines(lines, p_line)
            p_line = p_line + len(func_call_with_block_lines)
        elif line.find(': {') != -1:
            func_call_with_block_lines = get_closure_lines(lines, p_line)
            p_line = p_line + len(func_call_with_block_lines)
        elif line.find('({') != -1:
            func_call_with_block_lines = get_closure_lines(lines, p_line)
            p_line = p_line + len(func_call_with_block_lines)
        else:
            solve_line(line, deep)
            p_line = p_line + 1

solve_lines(lines, 'file', 0)