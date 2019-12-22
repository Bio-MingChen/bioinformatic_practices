#!/usr/bin/env python
# -*- coding=utf-8 -*-

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
        return gc_num / len(self.seq)

def FastqHandler(fastq_file,offset=33):
    """
    reading in fastq file and return read object
    """

    with open(fastq_file,'r') as indata:
        while True:
            line = indata.readline()
            if line:
                if not line.startswith('@'):
                    raise ValueError('Fastq File Format Error the title line does\'t start with @ Please check!')
                title_line = line.strip()
                seq_line = indata.readline()

                info_line = indata.readline()
                if not info_line or info_line[0] != "+":
                    raise ValueError('Info line should not be empty')
                
                bq_line = indata.readline() # only one line is allowed
                assert bq_line == seq_line ,'Base Quality line length differ from Base sequence line!'
                
                yield Read(title_line,seq_line,info_line,offset)
            else:
                break
            