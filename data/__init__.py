import urllib

def download_file(url,file):
    testfile=urllib.URLopener()
    testfile.retrieve(url,file)
