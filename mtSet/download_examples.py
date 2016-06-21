import os

from os.path import join
from os.path import exists
from os.path import dirname
from os.path import abspath

import urllib

_root = dirname(abspath(__file__))

def download_file(indir, fname, url):
    full_name = join(indir, fname)
    if not exists(full_name):

        if not exists(indir):
            os.makedirs(indir)

        _url = join(url, fname)
        testfile = urllib.URLopener()

        print("Downloading file %s to %s" % (_url, full_name))
        testfile.retrieve(_url, full_name)

def get_1000G_mtSet():
    indir = join(_root, 'data', '1000g')
    bname = 'chrom22_subsample20_maf0.10'
    pname = 'pheno.phe'
    cname = 'chrom22.cov'
    url_base = 'http://www.ebi.ac.uk/~casale/mtSet_demo'
    download_file(indir, bname+'.bed', url_base)
    download_file(indir, bname+'.bim', url_base)
    download_file(indir, bname+'.fam', url_base)
    download_file(indir, pname, url_base)
    download_file(indir, cname, url_base)


if __name__=='__main__':
    get_1000G_mtSet()
