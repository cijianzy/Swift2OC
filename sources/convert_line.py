# -*- coding: UTF-8 -*-
# Title: convert_line
# Time: 07/03/2018 4:52 PM
# Author: cijian
# Email: cijianzy@gmail.com

import sources.utility as utility
import re
def solve_line(line, deep):
    if line.find('import') != -1:
        line = line.replace('import', '@import') + ';'
    line = resolve_line(line)
    utility.append_to_body(line, deep)

def resolve_expression(line):
    m = re.match('"(.+?)"',line)
    if m:
        print(m.group(0))
    # if (m = re.match('(.+?)"(.+?)"(.+?)', line).group(1)) != None:
    #     return
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
    return line