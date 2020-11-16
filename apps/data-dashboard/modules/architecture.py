import re

from __init__ import ARCHITECTURE_FILE


def get_modules():
    arch_file = open(ARCHITECTURE_FILE, "r")
    lines = arch_file.readlines()
    arch_file.close()
    header = None

    modules = []

    for line in lines:

        regex = re.search(r'^# (\w+)', line)
        if regex and regex.group(1):
            header = regex.group(1)
            continue

        if header == 'modules':
            regex = re.search(r'^(\w+)', line)
            if regex and regex.group(1):
                modules.append(regex.group(1))

    return modules


def get_mapping():
    arch_file = open(ARCHITECTURE_FILE, "r")
    lines = arch_file.readlines()
    arch_file.close()
    header = None

    mappings = {}

    modules = get_modules()

    for module in modules:
        mappings[module] = []

    for line in lines:

        regex = re.search(r'^# (\w+)', line)
        if regex and regex.group(1):
            header = regex.group(1)
            continue

        if header == 'mapping':
            regex = re.search(r'^(\w+) (.+)', line)
            if regex and modules.index(regex.group(1)) + 1:
                mappings[regex.group(1)].append(regex.group(2))

    return mappings
