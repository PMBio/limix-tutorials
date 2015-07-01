import os
import urllib

def download_file(indir, fname, url):
    full_name = os.path.join(indir, fname)
    if not os.path.exists(full_name):
        if not os.path.exists(indir):   os.makedirs(indir)
        _url = os.path.join(url, fname)
        testfile = urllib.URLopener()
        testfile.retrieve(_url, full_name)
        print 'File %s does not exist. The file has been downloaded' % full_name
    else:
        print 'File %s exsits' % full_name

def get_1000G_mtSet():
    indir = './../data/1000g'
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

