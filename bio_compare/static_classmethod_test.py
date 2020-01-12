#!/usr/bin/env python
# -*- coding=utf-8 -*-
from prettytable import PrettyTable

class Test():
    a = 1
    b = 2
    # def __init__(self):
    #     self.a = 1
    #     self.b = 2
    
    @classmethod
    def classmethod_example(cls,a):
        print(cls.a)
        print(cls.b)
        print(a)
    
    # @staticmethod
    # def staticmethod_example(a):
    #     print(a)

if __name__ == "__main__":
    # test = Test()
    # Test.classmethod_example(3)
    # print(Test.staticmethod_example(3))
    pt = PrettyTable()
    pt.add_row(['a','1'])
    pt.add_row(['b','2'])
    pt.add_row(['c','3'])
    pt.add_row(['d','4'])
    print(pt)
