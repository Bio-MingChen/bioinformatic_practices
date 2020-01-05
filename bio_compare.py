#!/usr/bin/env python
# -*- coding=utf-8 -*-

#This tools is used to compare two files by one or more columns as key
# key is specified by user. one or more key can be stored in a config 
# file and you can use one of them whenever you need

# output can be customized and you can show arbitrary columns in the 
# result file extracted from the A or B file

import argparse

class CompareObj():
    """
    CompareObj represent a file which contains content of file like title
    and rows or columns and some functions to compare with other CompareObj
    """
    def __init__(self,filename):
        self.name = filename
    
    def get_title(self):
        pass

    def get_columns(self):
        pass

    def get_rows(self):
        pass

    def iter_row(self):
        pass

    def compare(self,compareobj):
        pass