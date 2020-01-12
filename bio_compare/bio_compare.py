#!/usr/bin/env python
# -*- coding=utf-8 -*-

#This tools is used to compare two files by one or more columns as key
# key is specified by user. one or more key can be stored in a config 
# file and you can use one of them whenever you need

# output can be customized and you can show arbitrary columns in the 
# result file extracted from the A or B file

import os
import sys
import json
import argparse
from collections import OrderedDict
from utilities import TitleParser,gopen,basic_log,make_colors
from prettytable import PrettyTable

# start log
logger = basic_log('bioCompare')

#init colors

colors = make_colors()

class KeyLib():
    """
    KeyLib offer generating,reading,writing and 
    extracting functions to the lib key
    """
    def __init__(self):
        self.config = os.path.join(os.environ['HOME'],'.keylib')
        self.init_keys = {
            'site': 'chrom,pos,ref,alt',
            'pos' : 'chrom,pos',
            }
        self.config_dict = {}

    def check(self):
        """
        whether .keylib is exist in your home directory
        """
        if not os.path.exists(self.config):
            logger.error('No .keylib file exists in your root directory!')
            logger.info('write a new .keylib file...')
            self.config_dict = self.init_keys
            logger.info('Create a new config with {config_dict}'.format(
            config_dict=self.config_dict))
            self._write()
        else:
            logger.info('reading config file .keylib ...')
            self._read()
        
    def _read(self):
        """
        reading in config file .keylib
        """
        with open(self.config,'r') as indata:
            self.config_dict = json.load(indata)

    def add(self,key,value):
        """
        Update {key:value} to  .keylib config
        """
        self.check()
        logger.info('Update {key}: {value} to ~/.keylib config...')
        self.config_dict.update({key:value})
        config_json = json.dumps(self.config_dict,indent=2,ensure_ascii=False)
        print('update result dict:\n{green}{bright}{config_json}{back}'.format(
            config_json=config_json,**colors))
        self._write()

    def remove(self,key):
        """
        Remove indicated value from ~/.keylib
        """
        self.check()
        if self.config_dict.get(key):
            del self.config_dict[key]
            self._write()
            logger.info('{key} have been removed from ~/.keylib!'.format(key=key))
            config_json = json.dumps(self.config_dict,indent=2,ensure_ascii=False)
            print('{green}{bright}{config_json}{back}'.format(
            config_json=config_json,**colors))
        else:
            logger.warning('{key} you want to remove from ~/.keylib doesn\'t exists!'.format(key=key))

    def _write(self):
        """
        write a new config with init_keys
        """
        with open(self.config,'w') as indata:
            json.dump(self.config_dict,indata,indent=2,ensure_ascii=False)

    def show(self):
        """
        show the content of .keylib
        """
        self.check()
        config_json = json.dumps(self.config_dict,indent=2,ensure_ascii=False)
        print("{green}{bright}{config_json}{back}".format(config_json=config_json,**colors))

    def __getitem__(self,tag):
        """
        reading config file and generate
        config_dict and get item from it
        """
        self.check()
        key = self.config_dict.get(tag)
        if key:
            return key
        else:
            logger.error('No such key!')
            self.show()
            return None 

class MainPipeline():
    """
    In order to decrease argument repeat use, parse
    them at the stage of initialization 
    """
    def __init__(self,args):

        #keylib and key handler
        self.keylib = KeyLib()
        #show key lib
        self.show_key_lib = args.get('show_key_lib')
        if self.show_key_lib:
            self.keylib.show()
            exit(0)
        #add key lib
        self.add_key = args.get('add_key')
        if self.add_key:
            if len(self.add_key.split(':')) == 2:
                key,value = self.add_key.split(':')
                self.keylib.add(key,value)
                exit(0)
            else:
                logger.error('Wrong add format,please input "key:value" format to add')
                exit(1)
        # remove key lib
        self.remove_key = args.get('remove_key')
        if self.remove_key:
            self.keylib.remove(self.remove_key)
            exit(0)
        #get key lib
        self.key = args.get('key')
        self.libkey = args.get('libkey')
        self.whole_line_as_key = False
        if (not self.key) and (not self.libkey):
            self.whole_line_as_key = True
            logger.info('Argument --key/-k or --libkey/-l are not assigned, all line will be as key')
        elif not self.key:
            self.key = self.keylib[self.libkey].split(',')
        else:
            self.key = self.key.split(',')
        #mode
        self.output_mode = args.get('output_mode')
        for i in self.output_mode:
            if i not in '123':
                logger.error('--output-mode should all or part of 123 {i} is invalid!'.format(i=i))
                exit(1)
        #reverse mode for example if 12 present in command line,self.mode will be 3
        self.mode = "".join([i for i in '123' if i not in self.output_mode])

        self.skip = args.get('skip')
        self.prefix = args.get('output')
        self.delimiter = args.get('delimiter')

        #reading A B file and get A_dict and B_dict
        self.A_file = args.get('A')
        self.B_file = args.get('B')
        self.A_dict,self.A_title = self.read_file(self.A_file)
        self.B_dict,self.B_title = self.read_file(self.B_file)

    def read_file(self,filename):
        """
        reading in file and generating dict
        by key
        """
        file_dict = OrderedDict()
        with open(filename,'r') as indata:
            # skip top lines with skip markers
            while True:
                line = indata.readline()
                if self.skip:
                    if line.startswith(skip):
                        continue
                title = line
                # print('Title is {title}'.format(title=title))
                tp = TitleParser(title)
                break
            for line in indata:
                line_list = line.strip().split(self.delimiter)
                # if key is all line will be as key
                if self.whole_line_as_key:
                    key = tuple(line_list)
                else:
                    key = tuple([tp.get_field(line_list,k,check=False) for k in self.key])
                if key in file_dict:
                    file_dict[key].append(line)
                else:
                    file_dict[key] = [line]

        return file_dict,title

    def compare(self):
        """
        compare A and B
        """
        A_set = { key for key in self.A_dict }
        B_set = { key for key in self.B_dict }

        # compare
        A_only = A_set - B_set
        B_only = B_set - A_set
        share = A_set & B_set
        #stat
        A_key_num = len(self.A_dict)
        B_key_num = len(self.B_dict)
        A_line_num = sum([len(value) for _,value in self.A_dict.items()])
        B_line_num = sum([len(value) for _,value in self.B_dict.items()])
        A_only_num = len(A_only)
        B_only_num = len(B_only)
        share_num = len(share)
        A_only_line_num = sum([len(self.A_dict[key]) for key in A_only])
        B_only_line_num = sum([len(self.B_dict[key]) for key in B_only])
        stat_value = [A_key_num,B_key_num,
            A_line_num,B_line_num,
            A_only_num,B_only_num,
            A_only_line_num,B_only_line_num,
            share_num]
        statnames = ['A key num','B key num',
            'A line num',' B line num',
            'A-only key num','B-only key num',
            'A-only line num','B-only line num',
            'Share num']
        pt = PrettyTable()
        pt.field_names = ['StatNames','Value']
        for name,value in zip(statnames,stat_value):
            pt.add_row([name,value])
        print('{green}{bright}{pt}{back}'.format(pt=pt,**colors))

        return A_only,B_only,share

    def write_func(self,filename,title,keys,key_dict):
        with open(filename,'w') as odata:
            odata.write(title)
            for key in keys:
                for line in key_dict[key]:
                    odata.write(line)

    def write_output(self,A_only_keys,B_only_keys,share_keys):
        """
        output to files by the mode type
        mode = [1,2,3]
        """
        if self.mode:
            if '1' in self.mode:
                A_only_file = self.prefix + '.A_only.xls'
                self.write_func(A_only_file,self.A_title,A_only_keys,self.A_dict)
                logger.info('A only file generated to {red}{bright}{A_only_file}{back} ...'.format(
                    A_only_file=A_only_file,**colors))
            if '2' in self.mode:
                B_only_file = self.prefix + '.B_only.xls'    
                self.write_func(B_only_file,self.B_title,B_only_keys,self.B_dict)
                logger.info('B only file generated to {red}{bright}{B_only_file}{back} ...'.format(
                    B_only_file=B_only_file,**colors))
            if '3' in self.mode:
                share_file = self.prefix + '.share.xls'
                self.write_func(share_file,self.A_title,share_keys,self.A_dict)
                logger.info('share file generated to {red}{bright}{share_file}{back} ...'.format(
                    share_file=share_file,**colors))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-A','-a',help='main file present in A only line and Share line')
    parser.add_argument('-B','-b',help='file B used to be compared with A file,present in B only line')
    parser.add_argument('--key','-k',help='key\'s to compare,comma split if -k and -l are not assigned, whole line will be as key')
    parser.add_argument('--libkey','-l',help='the name of some key in the libkey')
    parser.add_argument('--output-mode','-O',default='',
        help='''output mode,same with comm,default output: A only line\\t\\tB only line\\t\\t Share line
        1 suppress A only line and 2 suppress B only 3 suppress Share line
        ''')
    parser.add_argument('--output','-o',default="keycomm",help='output file prefix,default is keycomm')
    parser.add_argument('--show-key-lib','-show',action='store_true',help='show your current available key lib')
    parser.add_argument('--add-key','-add',help='add a new key to your key lib,format "key:value"')
    parser.add_argument('--remove-key','-rm',help='remove a key to your key lib')
    parser.add_argument('--skip','-skip',help='skip top lines with marker,for example indicate marker of # will skip lines startswith #')
    parser.add_argument('--delimiter','-d',default='\t',help='delimiter of field default \\t')
    args = vars(parser.parse_args())
    # print(args)
    main = MainPipeline(args)
    # compare A and B and output stat
    A_only,B_only,share = main.compare()
    # output result
    main.write_output(A_only,B_only,share)