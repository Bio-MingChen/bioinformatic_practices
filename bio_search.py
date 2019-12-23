#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Purporse:
# Search by several columns
# Columns can by get by title name or index
# Execute different operations like inclusion exclusion
# Add extra columns in results

# multiple files search (not update this time)

import argparse

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

class SearchQuery():
    """
    SearchQuery offer several functions
    get the query columns
    make query dict
    find out the search columns
    retain the extra content
    write result to ofile
    """
    def __init__(self,args):
        self.infile = args.get('infile')
        self.query_file = args.get('query')
        self.columns = args.get('columns')
        if self.columns:
            self.columns = args.get('columns').split(',')
        self.ofile = args.get('ofile')
        self.exclude = args.get('exclude')

    def get_search_key(self,tp,line_list):
        search_key = []
        for c in self.columns:
            search_column = tp.get_field(line_list,c)
            if not search_column:
                raise ValueError (
                    'Can\'t find the search column {} !'.format(c)
                )
            search_key.append(search_column)
        return tuple(search_key)

    def build_query_set(self):
        self.query_set = set()
        with open(self.query_file,'r') as indata:
            title = indata.readline()
            tp = TitleParser(title)
            for line in indata:
                line_list = line.strip().split('\t')
                search_key = self.get_search_key(tp,line_list)
                self.query_set.add(tuple(search_key))
            return self.query_set

    def filter(self):
        with open(self.infile,'r') as indata,\
        open(self.ofile,'w') as odata:
            title = indata.readline()
            odata.write(title)
            tp = TitleParser(title)
            for line in indata:
                line_list = line.strip().split('\t')
                search_key = self.get_search_key(tp,line_list)
                if not self.query_set:
                    raise ValueError ('query set is empty!')
                if search_key in self.query_set and (not self.exclude):
                    odata.write(line)
                if (not search_key in self.query_set) and self.exclude:
                    odata.write(line)
        print('write result to {}'.format(self.ofile))
    
    def main(self):
        self.build_query_set()
        self.filter()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile','-i',help='search files')
    parser.add_argument('--query','-q',help='search content stored in a file')
    parser.add_argument('--columns','-c',help='which columns should be as search query,CaseIgnore')
    parser.add_argument('--columns_query','-cq',help='''
    if this option is present,columns indicated by this argument
    will be as search query in query file,otherwise --columns argument
    will be used in both search infile and query file''')
    parser.add_argument('--search_index','-si',help='search file by several columns\' index 0-base')
    parser.add_argument('--query_index','-qi',help='indicating query file columns by their column index 0-base')
    parser.add_argument('--ofile','-o',help='output file')
    parser.add_argument('--exclude','-e',action='store_true',help='exclude other than include the lines')
    args = vars(parser.parse_args())
    print(args)
    if args.get('columns') and args.get('search_index'):
        raise ValueError ('--columns and --search_indx can\'t present at the same time')
    if args.get('columns_query') and args.get('query_index'):
        raise ValueError (
            '--columns_query and --query_index can\'t present simultaneously '
        )
    search_query = SearchQuery(args)
    search_query.main()