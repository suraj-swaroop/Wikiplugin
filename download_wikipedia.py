import requests
import shutil
import gzip
import bz2
import os
import re
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm


# Download wikipedia dataset
def download_file(filename, path):
    local_filename = filename.split('/')[-1]
    downloadPath = path + "/" + local_filename
    print('Started downloading: ', local_filename)
    
    try:
        # NOTE the stream=True parameter below
        with requests.get(filename, stream=True) as r:
            r.raise_for_status()

            # Total size in bytes.
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            t=tqdm(total=total_size, unit='iB', unit_scale=True)

            with open(downloadPath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size): 
                    if chunk: # filter out keep-alive new chunks
                        t.update(len(chunk))
                        f.write(chunk)
                        f.flush()
            t.close()
            if total_size != 0 and t.n != total_size:
                print("ERROR, something went wrong")

        print('Finished downloading.')
        return 0
    except:        
        return 1


# Checking a directory
def check_paht(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Create download paths. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Creation of the directory %s failed" % inputPath)
        sys.exit(1)
    else:
        print ("Successfully created the directory %s" % inputPath)
          
        
def clickstream(date):
    url = 'https://dumps.wikimedia.org/other/clickstream/'
    input_date = date[:4]+'-'+date[4:]
    file_page = url+input_date+'/'
    res_page = requests.get(file_page)
    content_page = str(res_page.text)
    html_page = BeautifulSoup(content_page, 'html.parser')
    container_link = html_page.find_all('a', href=True, text=True)
    
    en_file = ''
    for link in container_link:
        if ('-enwiki-' in link.text):
            en_file = link.text

    filename = file_page+en_file    
    path = "./download/clickstream"
    check_paht(path)
    
    download_file(filename, path)
    return 0


def text(date, index):
    url = 'http://dumps.wikimedia.your.org/other/pageviews/'

    available_files = []
    file_page = url + date[0:4] + '/' + date[0:4] + "-" + date[4:6]

    res_page = requests.get(file_page)
    content_page = str(res_page.text)
    html_page = BeautifulSoup(content_page, 'html.parser')
    for a in html_page.find_all('a', href=True):
        available_files.append(a['href'])

    filename = file_page+"/"+available_files[int(index)]
    path = "./download/pageview"
    check_paht(path)
    
    download_file(filename, path)

    return 0
    
#     print('Now decompressing the file...')

#     comp_file = bz2.BZ2File(local_file, 'rb')
#     read_file = comp_file.read()
#     comp_file.close()

#     new_file_name = '-'.join(local_file.split('-')[:-1])
#     f =  open(new_file_name, 'wb')
#     f.write(read_file)
#     f.close()

#     shutil.move(new_file_name, 'Datasets/'+new_file_name)
#     os.unlink(local_file)
#     print('Finished decompressing the file.')

    
if __name__ == '__main__':
    # Check arguments
    if len(sys.argv) < 2:
        print("[Error] Invalid input")
        sys.exit(1)

    data = (sys.argv[1]).split(":")
    dataType = data[0]
    date = data[1]
    index = data[2]
    print("[Input] date:[{}], index:[{}], type:[{}]".format(date, index, dataType))

    if dataType == 'clickstream':
        clickstream(date)
    elif dataType == 'text':
        text(date, index)

# End of main
