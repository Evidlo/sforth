#!/bin/env python3

import sys

filename = sys.argv[1]

code = open(filename, 'r').read().split()
pointer = 0

stack = []

def check_types(args, types, err=""):
    for arg in args:
        assert type(arg) in types, err

while pointer < len(code):

    # --- string ---
    if code[pointer].startswith('"') and code[pointer].endswith('"'):
        stack.append(code[pointer].strip('"'))

    # --- integer ---
    if code[pointer].isnumeric():
        stack.append(int(code[pointer]))

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
        code.pop(pointer)
        repeat_num = stack.pop()
        assert type(repeat_num) is int, "`repeat` must be preceded by integer"
        repeat_item = stack.pop()
        for _ in range(repeat_num):
            if type(repeat_item) is list:
                code[pointer:pointer] = repeat_item
            else:
                code.insert(pointer, repeat_item)
        pointer -= 1

    # --- dup ---
    elif code[pointer] == 'dup':
        dup_depth = stack.pop()
        check_types([dup_depth], [int], "`dup` must be preceded by numeric")
        stack += stack[-dup_depth:]

    # -- dumpstack ---
    elif code[pointer] == 'printstack':
        print(stack)

    # --- print ---
    elif code[pointer] == 'print':
        print_item = stack.pop()
        print(print_item)

    # --- add ---
    elif code[pointer] == 'add':
        item1 = stack.pop()
        item2 = stack.pop()
        check_types((item1, item2), (float, int), "`add` takes 2 numerics")
        stack.append(item2 + item1)

    # --- sub ---
    elif code[pointer] == 'sub':
        item1 = stack.pop()
        item2 = stack.pop()
        check_types((item1, item2), (float, int), "`sub` takes 2 numerics")
        stack.append(item2 - item1)

    # --- mul ---
    elif code[pointer] == 'mul':
        item1 = stack.pop()
        item2 = stack.pop()
        check_types((item1, item2), (float, int), "`mul` takes 2 numerics")
        stack.append(item2 * item1)

    # --- div ---
    elif code[pointer] == 'div':
        item1 = stack.pop()
        item2 = stack.pop()
        check_types((item1, item2), (float, int), "`div` takes 2 numerics")
        stack.append(item2 / item1)

    pointer += 1
    if False:
        print('----------------')
        print(code[pointer:])
        print(stack)
        input()
