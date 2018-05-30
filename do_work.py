#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
from app import models

def main():
    FORMAT = "%(asctime)s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel("INFO".upper())

    command_fuc = {
        'init_table':models.init_table,
    }

    if len(sys.argv) > 1:
        if command_fuc.get(sys.argv[1]):
            command_fuc.get(sys.argv[1])()
        else:
            print('command not find')


    else:
        print('可输入以下命令:')
        print('-----')
        for i in command_fuc:
            print(i)
        print('-----')
if __name__ == "__main__":
    main()
