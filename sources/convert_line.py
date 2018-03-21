# -*- coding: UTF-8 -*-
# Title: convert_line
# Time: 07/03/2018 4:52 PM
# Author: cijian
# Email: cijianzy@gmail.com

import sources.utility as utility
import re

def contain_func_call(line):
    fragments = line.split(' ')
    # SnapKit
    if line.find('make') != -1 and line.find('equalTo') != -1:
        return False
    for f in fragments:
        if f.find('.') != -1 and f.find('(') != -1:
            return True
    return False

def solve_line(line, deep):
    if line.find('import') != -1:
        line = line.replace('import', '@import') + ';'
    line = resolve_line(line)
    utility.append_to_body(line, deep)

def resolve_func(line):
    if line.find(')') != -1:
        r = line.find(')')

        l = len(line) - line[::-1].find('(')
        # print(line[::-1])
        # print(l, r)
        print(line[l-1:r+1])
    return line

def resolve_expression(line):
    # solve expression
    m = re.match('"(.+?)"',line)
    if m:
        return '@"{}"'.format(m.group(1))
    m = re.search('([a-zA-Z]+)\(\)', line)
    if m and line.find('.') == -1:
        return '[[{} alloc] init];'.format(m.group(1))
    # this if is to ship snpkit equalto, because it's not like normal function
    if line.find('euqalTo') != -1:
        return line
    if contain_func_call(line):
        line = resolve_func(line)

    return line

def resolve_init(line):
    pre = line.split('=')[1].split('(')[0].strip() + ' *' + line.split('=')[0].split(' ')[1] + ' = '
    return pre + resolve_expression(line.split('=')[1].strip()) + ';'

def resolve_equal(line):
    return resolve_expression(line.split('=')[0].strip()) + ' = ' + resolve_expression(line.split('=')[1].strip()) + ';'

def resolve_line(line):
    if line.find('let') == 0:
        return resolve_init(line)
    if line.find(' = ') != -1:
        return resolve_equal(line)
    if line.find('return') == 0:
        return 'return ' + resolve_expression(line.split(' ')[1]) + ';';
    return resolve_expression(line) + ';'