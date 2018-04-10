# -*- coding: UTF-8 -*-
# Title: convert_line
# Time: 07/03/2018 4:52 PM
# Author: cijian
# Email: cijianzy@gmail.com

import sources.utility as utility
import re
import random
import string

replace_map = {}

def contain_func_call(line):
    fragments = line.split(' ')
    # SnapKit make function, it use block to replace function, so there should ship this case
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


def resolve_func_call_with_no_params(line):
    line = '[' + resolve_func_call('.'.join(line.split('.')[:-1])) + ' ' + line.split('.')[-1][:-2] + ']'
    return line


def resolve_func_call_with_params(line):
    """
    resolve function call
    :param line: function call
    :return: resolved function call
    """

    if line.find('#select') == 0:
        result_line = line.replace('#', '@')
    elif line.find('.aly') != -1:
        result_line = line
    elif re.search(r'\(([A-Za-z0-9_]+)\)', line) != None:
        result_line = '[' + resolve_func_call('.'.join(line.split('.')[:-1])) + ' ' + line.split('.')[-1][:-1] + ']'
        result_line = result_line.replace('(', ': ')
    elif re.search(r'\(([A-Za-z0-9_. :,]+)\)', line) != None:
        re_result = re.search(r'\(([A-Za-z0-9_.: ,]+)\)', line)
        span = re_result.span()
        func_param_l = line.find('(')
        func_param_r = line.find(')')
        func_call = line[:func_param_l]
        # get params
        func_params = line[func_param_l+1:func_param_r]

        params_array = func_params.split(',')

        result_line = '[' + func_call

        if params_array[0].find(':') == -1:
            result_line += ':'
        elif params_array[0].find('With') != -1:
            pass
        # else:
        #     result_line += 'With'

        for param in params_array:
            result_line += param
        result_line += ']'
    return result_line

def resolve_func_call(line):

    if line.find(')') != -1:
        # solve option symbols
        line = line.replace('?.', '.')
        line = line.replace(')?', ')')

        func_r = line.find(')')

        # print(line[r+1::-1])
        call_l = func_r - line[func_r+1::-1].find('(')
        func_l = call_l

        for i in range(call_l-1, -1 ,-1):
            if line[i] != '(' and line[i] != ' ':
                func_l = i
            else:
                break
        func_line = line[func_l: func_r+1]
        if func_line[-2:] == '()':
            # Need get random str to avoid while replace loop
            line = line[:func_l] + get_random_str(resolve_func_call_with_no_params(func_line)) + line[func_r+1:]
        else:
            line = line[:func_l] + get_random_str(resolve_func_call_with_params(func_line)) + line[func_r+1:]

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
    while contain_func_call(line):
        line = resolve_func_call(line)

    return line

def resolve_init(line):
    pre = line.split('=')[1].split('(')[0].strip() + ' *' + line.split('=')[0].split(' ')[1] + ' = '
    return pre + resolve_expression(line.split('=')[1].strip())

def resolve_equal(line):
    return resolve_expression(line.split('=')[0].strip()) + ' = ' + resolve_expression(line.split('=')[1].strip())

def get_random_str(line):
    global replace_map
    map_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
    replace_map[map_str] = line
    return map_str

def resolve_line(line):
    global replace_map

    replace_map = {}

    result = ''

    if line.find('let') == 0:
        result = resolve_init(line)
    elif line.find(' = ') != -1:
        result = resolve_equal(line)
    elif line.find('return') == 0:
        result = 'return ' + resolve_expression(line.split(' ')[1]);
    else:
        result = resolve_expression(line)

    has_replace_key = True
    while has_replace_key:
        has_replace_key = False
        for key in replace_map.keys():
            if result.find(key) != -1:
                result = result.replace(key, replace_map[key])
                has_replace_key = True
    return result + ';'