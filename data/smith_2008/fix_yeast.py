import numpy as SP
import tables
import pandas as pd
import limix.modules.data_util as du

fixit = False

def checkchroms(chrom, pos):
    chromvals = SP.unique(chrom)#SP.unique is always sorted
    chrom_max=SP.zeros_like(chromvals)#get the starting position of each Chrom
    chrom_last=SP.zeros_like(chromvals)#get the starting position of each Chrom
    position_fix=pos.copy()#get the starting position of each Chrom
    notsorted=SP.zeros_like(chromvals,dtype='bool')#get the starting position of each Chrom
    for i,mychrom in enumerate(chromvals):
        i_chr=chrom==mychrom
        last = -1
        for snp in xrange(len(pos)):
            if i_chr[snp]:
                if last>pos[snp]:
                    notsorted[i]=True
                last=pos[snp]
                if notsorted[i]:
                    position_fix[snp]+=1000000
                                    
        chrom_max[i] = pos[i_chr].max()
        chrom_last[i] = pos[i_chr][-1]
    return chrom_max,notsorted,chrom_last,position_fix

if fixit:
    f =  tables.open_file("smith08.hdf5","a")
else:
    f =  tables.open_file("smith08.hdf5","r")
pos = f.root.genotype.col_header.pos[:]
pos_cum = f.root.genotype.col_header.pos_cum[:]
chrom = f.root.genotype.col_header.chrom[:]
chrom_max,notsorted,chrom_last,pos_fix = checkchroms(chrom,pos)
chrom_max_fix,notsorted_fix,chrom_last_fix,pos_fix_fix = checkchroms(chrom,pos_fix)

position = pd.DataFrame(data=SP.array([pos,chrom]).T,columns = ['pos','chrom'])
chrom_len = [230218,813184,316620,1531933,576874,270161,1090940,562643,439888,745751,666816,1078177,924431,784333,1091291,948066]
chrom_pos_cum = du.estCumPos(position, offset=0,chrom_len=chrom_len)
if fixit:
    f.root.genotype.col_header.pos[:]=pos_fix[:]
    f.root.genotype.col_header.pos_cum[:]=position["pos_cum"].values[:]