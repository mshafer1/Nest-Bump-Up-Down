#!/usr/bin/env python3

'''
Python3, entry point to request the thermostat shift down slightly. See Readme for reference use with Apache or NginX

'''

# -*- coding: UTF-8 -*-
import nest_utils
# enable debugging
import cgitb
cgitb.enable()

import logging

_module_logger = logging.getLogger(__name__)
_module_logger.addHandler(logging.NullHandler())


def main():
    print("Content-Type: text/plain;charset=utf-8")
    print('')

    try:
        _module_logger.info('Attempting to bump down')
        nest_utils.bump_down()
        print('ACK')
        _module_logger.info('Success')
    except Exception as e:
        print('Fail')
        _module_logger.info('Error')
        _module_logger.error(e)


if __name__ == '__main__':
    _module_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('_log.txt')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    _module_logger.addHandler(fh)
    
    main()