#!/usr/bin/env python
# -*- coding=utf-8 -*-

import argparse
from collections import Counter,defaultdict,namedtuple
import numpy as np

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
        self.counter = Counter(self.qual)
        self.aver_qual = np.mean(self.qual)

    def __len__(self):
        return len(self.seq)

    def __getitem__(self,idx):
        base = namedtuple('base',['seq','qual'])
        return base(self.seq[idx],self.qual[idx])

    def N_number(self):
        return len([base for base in seq if base == 'N'])
    
    def gc(self):
        gc_num = [base for base in self.seq if base in ['G','g','C','c']]
        if len(self.seq) == 0: #handling ZeroDivisionError
            return 0
        return float(gc_num) / len(self.seq)

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
    nreads = 0
    N_numbers = 0
    qual_class = {}
    for read in FastqHandler(fastq_file):
        if len(read.qual) != query_len:
            print(len(read.qual))
            print(read.qual)
            raise FastqError('Read {readid} length is not {length}'.format(
            readid = read.id,length=query_len))
        BQ_query += read.qual
        N_numbers += read.N_number
        nreads += 1
        for key,value in read.counter
    print(BQ_query)
    all_bases = nreads*query_len
    return BQ_query

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fastq','-fq',help="fastq file")
    parser.add_argument('--read_length','-l',type=int,default=150,
        help="read length default is 150")
    args = parser.parse_args()
    main(vars(args))
            