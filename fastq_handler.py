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
        if len(self.seq) == 0:
            return 0
        return gc_num / len(self.seq)

def FastqHandler(fastq_file):
    """
    reading in fastq file and return read object
    """
    with open(fastq_file,'r') as indata:
        for line in indata:
