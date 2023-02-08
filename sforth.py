#!/bin/env python3

import sys

filename = sys.argv[1]

code = open(filename, 'r').read().split()
pointer = 0

stack = []

def check_types(args, types, err=""):
    if type(args) not in (list, tuple):
        args = [args]
    if type(types) not in (list, tuple):
        types = [types]
    for arg in args:
        assert type(arg) in types, f"Expected {types}. Got {[type(arg) for arg in args]}"

def insert_code(code, pointer, item):
    if type(item) is list:
        code[pointer:pointer] = [str(i) for i in item]
    else:
        code.insert(pointer, str(item))

while pointer < len(code):

    # --- string ---
    if code[pointer].startswith('"') and code[pointer].endswith('"') and len(code[pointer]) >= 2:
        stack.append(code[pointer].strip('"'))

    # --- integer ---
    elif code[pointer].isnumeric():
        stack.append(int(code[pointer]))

    # --- boolean ---
    elif code[pointer] in ("True", "False"):
        stack.append(code[pointer] == 'True')

    # --- group ---
    elif code[pointer] == '{':
        substack = []
        pointer += 1
        try:
            while code[pointer] != '}':
                substack.append(code[pointer])
                pointer += 1
        except IndexError:
            raise IndexError("Symbol group not closed!")
        stack.append(substack)

    # --- repeat ---
    elif code[pointer] == 'repeat':
        repeat_num = stack.pop()
        assert type(repeat_num) is int, "`repeat` must be preceded by integer"
        repeat_item = stack.pop()
        for _ in range(repeat_num):
            insert_code(code, pointer + 1, repeat_item)

    # --- dup ---
    elif code[pointer] == 'dup':
        dup_depth = stack.pop()
        check_types(dup_depth, int, "`dup` must be preceded by numeric")
        stack += stack[-dup_depth:]

    # -- dumpstack ---
    elif code[pointer] == 'printstack':
        print(stack)

    # --- print ---
    elif code[pointer] == 'print':
        print_item = stack.pop()
        print(print_item)

    elif code[pointer] == 'input':
        item1 = stack.pop()
        check_types(item1, str)
        insert_code(code, pointer + 1, f'"{input(item1)}"')
        # pointer += 1
        # stack.append(input('Input:'))

    # --- add ---
    elif code[pointer] == 'add':
        item2, item1 = stack.pop(), stack.pop()
        check_types((item1, item2), (float, int), "`add` takes 2 numerics")
        stack.append(item1 + item2)

    # --- sub ---
    elif code[pointer] == 'sub':
        item2, item1 = stack.pop(), stack.pop()
        check_types((item1, item2), (float, int), "`sub` takes 2 numerics")
        stack.append(item1 - item2)

    # --- mul ---
    elif code[pointer] == 'mul':
        item2, item1 = stack.pop(), stack.pop()
        check_types((item1, item2), (float, int), "`mul` takes 2 numerics")
        stack.append(item1 * item2)

    # --- div ---
    elif code[pointer] == 'div':
        item2, item1 = stack.pop(), stack.pop()
        check_types((item1, item2), (float, int), "`div` takes 2 numerics")
        stack.append(item1 / item2)

    # --- less than ---
    elif code[pointer] == 'lt':
        item2, item1 = stack.pop(), stack.pop()
        check_types((item1, item2), (float, int), "`div` takes 2 numerics")
        stack.append(item1 < item2)

    # --- ifelse ---
    elif code[pointer] == 'ifelse':
        item_else, item_if, item_condition = stack.pop(), stack.pop(), stack.pop()
        check_types(item_condition, bool, "`ifelse` argument 1 should be bool")
        if item_condition:
            insert_code(code, pointer + 1, item_if)
        else:
            insert_code(code, pointer + 1, item_else)

    else:
        raise ValueError(f"Invalid code object {code[pointer]}")

    pointer += 1
    if True:
        print('----------------')
        print('c:', code[pointer:])
        print('s:', stack)
        input()
