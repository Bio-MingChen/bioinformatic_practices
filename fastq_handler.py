#!/usr/bin/env python
# -*- coding=utf-8 -*-

import argparse
import gzip
from collections import Counter,defaultdict,namedtuple
import numpy as np
from prettytable import PrettyTable

class Read():
    """
    read object and it have some methods list below
    fqid : read id
    seq : read nucleotide sequence
    qual : Base Quality(BQ) sequence
    counter : BQ numbers counter
    aver_qual : Average Base quality
    gc : Average GC 
    N_number : N base number

    Note: This function dosen't consider adaptor up to now
    """
    def __init__(self,fqid,seq,qual,offset=33):
        self.id = fqid
        self.seq = seq
        self.qual = [ord(q)-offset for q in qual]
        self.qual_counter = Counter(self.qual)
        self.ATCG_counter = Counter(self.seq)
        self.aver_qual = np.mean(self.qual)

    def __len__(self):
        return len(self.seq)

    def __getitem__(self,idx):
        base = namedtuple('base',['seq','qual'])
        return base(self.seq[idx],self.qual[idx])

    def get_N_number(self):
        return len([base for base in self.seq if base == 'N'])
    
    def get_gc_num(self):
        gc_num = [base for base in self.seq if base in ['G','g','C','c']]
        if len(self.seq) == 0: #handling ZeroDivisionError
            return 0
        # return float(gc_num) / len(self.seq)
        return len(gc_num)

def gopen(filename,mode):
    """
    open .gz file with gzip.open
    open plain text file with open
    """
    if filename.endswith('.gz'):
        return gzip.open(filename,mode)

    return open(filename,mode)
class FastqError(Exception):
    """
    Customized Exception FastqError
    """
    def __init__(self,err='FastqError'):
        Exception.__init__(self,err)

def FastqHandler(fastq_file,offset=33):
    """
    reading in fastq file and return read object
    """

    with gopen(fastq_file,'r') as indata:
        while True:
            line = indata.readline()
            if line:
                if not line.startswith('@'):
                    raise FastqError('Fastq File Format Error the title line does\'t start with @ Please check!')
                title_line = line.strip()
                seq_line = indata.readline().strip()

                info_line = indata.readline()
                if not info_line or info_line[0] != "+":
                    raise FastqError('Info line should not be empty')
                
                bq_line = indata.readline().strip() # only one line is allowed
                # print(bq_line[150])
                # print(len(bq_line))
                # print(seq_line)
                # print(len(seq_line))    
                assert not bq_line == seq_line ,'Base Quality line length differ from Base sequence line!'
                
                yield Read(title_line,seq_line,bq_line,offset)
            else:
                break


def main(args):
    fastq_file = args.get('fastq')
    query_len = args.get('read_length')
    BQ_query = np.zeros(query_len)
    #initialize the stat variates
    nreads = 0
    N_numbers = 0
    qual_class = defaultdict(int)
    ATCG_stat = defaultdict(int)
    gc_num = 0
    # pretty table
    basic_table = PrettyTable()
    basic_table.field_names = ['Read Length','Reads Numbers','Base Numbers','N Numbers','GC Percent','A','T','C','G']
    class_table = PrettyTable()
    # position BQ table
    bq_table = PrettyTable()
    bq_table.field_names = ['Base Quality By Read Position']
    for read in FastqHandler(fastq_file):
        if len(read.qual) != query_len:
            print(len(read.qual))
            print(read.qual)
            raise FastqError('Read {readid} length is not {length}'.format(
            readid = read.id,length=query_len))
        BQ_query += read.qual
        N_numbers += read.get_N_number()
        nreads += 1
        gc_num += read.get_gc_num()
        for key,value in read.qual_counter.items():
            qual_class[key] += value
        for key,value in read.ATCG_counter.items():
            ATCG_stat[key] += value

    all_bases = nreads*query_len
    gc_percent = round(gc_num / all_bases,3)
    basic_table.add_row([query_len,nreads,all_bases,N_numbers,gc_percent,ATCG_stat['A'],ATCG_stat['T'],ATCG_stat['C'],ATCG_stat['G']])
    print(basic_table)
    #class table
    title_list = []
    row_list = []
    for key,value in qual_class.items():
        title_list.append(key)
        row_list.append(value)
    class_table.field_names = title_list
    class_table.add_row(row_list)
    print('The classification of Base Quality')
    print(class_table)

    bq_table.add_row([BQ_query])
    print(bq_table)
    return BQ_query

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fastq','-fq',help="fastq file")
    parser.add_argument('--read_length','-l',type=int,default=150,
        help="read length default is 150")
    args = parser.parse_args()
    main(vars(args))
            