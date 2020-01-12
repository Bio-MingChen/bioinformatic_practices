#show ~/.keylib
python2 bio_compare.py -show

#add key to keylib
python2 bio_compare.py -add "bed:chrom,start,end"

#remove key 
python2 bio_compare.py -rm bed

#compare A and B
python2 bio_compare.py -a merged.brief_result.article_CHIP.xls -b merged.brief_result.xls -k "sample,gene,chromosome,position"
python2 bio_compare.py -a merged.brief_result.article_CHIP.xls -b merged.brief_result.xls 

#A example to use KeyLib
python2 bio_compare.py -add "shanmu:sample,gene,chromosome,position"
python2 bio_compare.py -a merged.brief_result.article_CHIP.xls -b merged.brief_result.xls -l shanmu
