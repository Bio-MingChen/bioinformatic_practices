#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging
import gzip
import colorama

class TitleParser():
    """
    Reading in a file title and than getting indicated column element.
    Title names are all CaseIgnore
    """
    
    def __init__(self,title):
        self.title_list = [i.lower() for i in title.strip().split('\t')]

    def get_field(self,line_list,colname,check=True):
        """
        Reading in a list and returning the element with the 
        index which colname in title's list
        """
        if check:
            if len(self.title_list) != len(line_list):
                raise Exception("Title length differs with line!")
        try:
            idx = self.title_list.index(str(colname).lower())
        except:
            print('{colname} not in title！'.format(colname=colname))
            return None

        return line_list[idx]

    def have_title(self,colname):
        """
        Judging whether a colname is in title
        """
        if str(colname).lower() in self.title_list:
            return True
        return False
    
    def get_idx(self,colname):
        """
        return index of columns by their name in title list
        """
        idx = self.title_list.index(str(colname).lower())

        return idx

#=======================================
#gopen function is used to open file by their suffix
# open .gz file with gzip.open else open
#=======================================

def gopen(filename,mode):
    """
    open .gz file with gzip.open
    open plain text file with open
    """
    if filename.endswith('.gz'):
        return gzip.open(filename,mode)

    return open(filename,mode)

#=======================================
#basic_log set the basicConfig of logging and return a logger 
#========================================

def basic_log(name,level=logging.DEBUG,logfile=None,filemode="w",log_format=None):
    """
    Set basic logging config and name a logger
    """
    if not log_format:
        log_format = '[%(asctime)s:%(funcName)s:%(name)s:%(levelname)s] %(message)s'
    if logfile:
        logging.basicConfig(filename=logfile,level=level,
            filemode=filemode,format= log_format
            )
    else:
        logging.basicConfig(level=level,format=log_format)

    logger = logging.getLogger(name)

    return logger

def make_colors():
    """
    make some colors in command line
    """
    colors = {}
    colorama.init()
    colors['red'] = colorama.Fore.RED
    colors['green'] = colorama.Fore.GREEN
    colors['green_ex'] = colorama.Fore.LIGHTGREEN_EX
    colors['white'] = colorama.Fore.LIGHTWHITE_EX
    colors['magenta_ex'] = colorama.Fore.LIGHTMAGENTA_EX
    colors['magenta'] = colorama.Fore.MAGENTA
    colors['cyan'] = colorama.Fore.CYAN
    colors['cyan_ex'] = colorama.Fore.LIGHTCYAN_EX
    colors['yellow'] = colorama.Fore.YELLOW
    colors['bright'] = colorama.Style.BRIGHT
    colors['back'] = colorama.Style.RESET_ALL
    return colors