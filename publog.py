#!/usr/bin/env python
# -*- coding:utf-8 -*-
#制作:温赫男

'''公共日志
'''
import logging

def _joinmsg(msg,*args):
    data =[str(msg)]
    for arg in args:
        data.append(str(arg))
    return  ",".join(data)

def critical(msg, *args, **kwargs):
    newmsg = _joinmsg(msg,*args)
    logging.critical(newmsg, **kwargs)

fatal = critical

def error(msg, *args, **kwargs):
    newmsg = _joinmsg(msg,*args)
    logging.error(newmsg, **kwargs)

def exception(msg, *args, **kwargs):

    kwargs['exc_info'] = 1
    newmsg = _joinmsg(msg,*args)
    logging.exception(newmsg, **kwargs)

def warning(msg, *args, **kwargs):
    newmsg = _joinmsg(msg,*args)
    logging.warning(newmsg, **kwargs)

warn = warning

def info(msg, *args, **kwargs):
    newmsg = _joinmsg(msg,*args)
    logging.info(newmsg, **kwargs)

def debug(msg, *args, **kwargs):
    newmsg = _joinmsg(msg,*args)
    logging.debug(newmsg, **kwargs)

def log(level, msg, *args, **kwargs):
    newmsg = _joinmsg(msg,*args)
    logging.log(newmsg, **kwargs)