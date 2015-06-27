"""standard setup.py used by all tutorials
   This loads commonly used LIMIX functions
"""
import sys
sys.path.append('./..')
import data as tutorial_data


import scipy as sp
import pylab as pl
from matplotlib import cm
import scipy.stats as st
import h5py
import pdb
import pandas as pd
sp.random.seed(0)
# import LIMIX
import sys
import limix.modules.varianceDecomposition as var
import limix.modules.qtl as qtl
import limix.io.data as data
import limix.io.genotype_reader as gr
import limix.io.phenotype_reader as phr
import limix.io.data_util as data_util
import limix.utils.preprocess as preprocess
# plotting and visualization utilties
from limix.utils.plot import *
# genotype summary stats
from limix.deprecated.stats.geno_summary import *
import os
import cPickle
import sys
import numpy as np
import pandas as pd
