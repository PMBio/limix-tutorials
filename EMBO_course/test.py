
# coding: utf-8

## Setting up

# In[1]:

# activiate inline plotting


# In[2]:

import scipy as SP
import pylab as PL
from matplotlib import cm
import h5py
import pdb
import pandas as pd
SP.random.seed(0)


# In[3]:

# import LIMIX
import sys
import limix
import limix.modules.varianceDecomposition as VAR
import limix.modules.qtl as QTL
import limix.modules.data as DATA
import limix.modules.genotype_reader as gr
import limix.modules.phenotype_reader as phr
import limix.modules.data_util as data_util
import limix.utils.preprocess as preprocess
# plotting and visualization utilties
from limix.utils.util import *
from limix.utils.plot import plot_manhattan


# In[4]:

#import data
#the data used in this study have been pre-converted into an hdf5 file. 
#to preprocess your own data, please use limix command line brinary
file_name = './../data/arab107/Nordborg_data.h5py'

f = h5py.File(file_name,'r')
geno_id = SP.array(f['geno']['meta'][1::,4],dtype='int')
pheno_id = f['pheno']['ecotype_id'][:]

Igeno = SP.zeros([len(pheno_id)],dtype='int')
for i in xrange(len(pheno_id)):
    ii =SP.nonzero(geno_id==pheno_id[i])[0][0]
    Igeno[i] = ii

X = f['geno']['x'][:][:,Igeno].T
Y = f['pheno']['Y'][:]
phenotype_names = f['pheno']['phenotype_names'][:]
ipheno = SP.nonzero(phenotype_names=='5_FT10')[0][0]
y = Y[:,ipheno:ipheno+1]
Iok = ~SP.isnan(y[:,0])
y = y[Iok]
X = X[Iok]


# In[5]:
#import data
#the data used in this study have been pre-converted into an hdf5 file. 
#to preprocess your own data, please use limix command line brinary
file_name = './../data/arab107/atwell_107.hdf5'
geno_reader  = gr.genotype_reader_tables(file_name)
pheno_reader = phr.pheno_reader_tables(file_name)

#the data object allows to query specific genotype or phenotype data
data = DATA.QTLData(geno_reader=geno_reader,pheno_reader=pheno_reader)
#getting genotypes
snps = data.getGenotypes() #SNPs
position = data.getPos()
chromBounds = data_util.estCumPos(position=position,offset=100000)

# non-normalized and normalized sample relatedeness matrix
#sample_relatedness_unnormalized = data.getCovariance(normalize=False,center=False)
sample_relatedness_unnormalized = data.getCovariance(normalize=True,center=True)

sample_relatedness  = sample_relatedness_unnormalized/     sample_relatedness_unnormalized.diagonal().mean()


# In[6]:

X = SP.array(X,dtype='float')
#y = SP.array(y,dtype='float')
#K = sample_relatedness
K = SP.eye(snps.shape[0])
covs = SP.ones([X.shape[0],1])
test="lrt" 
lmm = QTL.test_lmm(snps=X,pheno=y,
                   K=K,covs=covs,test=test)

lmm2 = limix.CLMM()
lmm2.setSNPs(X)
lmm2.setPheno(y)
lmm2.setK(K)
lmm2.setCovs(covs)
#lmm2.setTestStatistics(lmm2.TEST_F)
lmm2.process()

pvalues_lmm = lmm.getPv()       # 1xS vector of p-values (S=X.shape[1])#convert P-values to a DataFrame for nice output writing:
pvalues_lmm2 = lmm2.getPv()

pdb.set_trace()

# In[9]:
PL.plot(-SP.log10(pvalues_lmm.ravel()))


# In[10]:

phenotype_query = "(phenotype_ID=='5_FT10')"
# getting the appropriate data subset
data_subsample = data.subsample_phenotypes(phenotype_query=phenotype_query,
                                           intersection=True)

#get variables we need from data
if 0:
    snps = data_subsample.getGenotypes(impute_missing=False,center=False)
    snps = SP.array(snps,dtype='float')
else:
    snps = data_subsample.getGenotypes(impute_missing=True,center=True)

phenotypes,sample_idx = data_subsample.getPhenotypes(phenotype_query=phenotype_query,
                                                     intersection=True,center=False) 
assert sample_idx.all()

snps-=snps.mean(axis=0)

#set parameters for the analysis
N, P = phenotypes.shape 
S    = snps.shape[1]

phenotypes = phenotypes.values

print "loaded %d samples, %d phenotypes, %s snps" % (N,P,S)

covs = None                 #covariates
searchDelta = False         #specify if delta should be optimized for each SNP
test="lrt"                  #specify type of statistical test

# Running the analysis
# when cov are not set (None), LIMIX considers an intercept (covs=SP.ones((N,1)))
K2 = sample_relatedness
K2 = SP.eye(snps.shape[0])
lmm2 = QTL.test_lmm(snps=snps,pheno=phenotypes,
                   K=K2,covs=covs, test=test)

pvalues_lmm2 = lmm.getPv()       # 1xS vector of p-values (S=X.shape[1])#convert P-values to a DataFrame for nice output writing: