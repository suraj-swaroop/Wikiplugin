import requests
import shutil
import gzip
import bz2
import os
import re
import sys
from bs4 import BeautifulSoup


def download_file(filename):
    local_filename = filename.split('/')[-1]
    print('Started downloading: ', local_filename)
    print('It may take up to 10 minutes to complete the process.')
    with requests.get(filename, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


def clickstream(data_type, input_date):
	url = 'https://dumps.wikimedia.org/other/clickstream/'
	res = requests.get(url)
	content = str(res.text)
	html_soup = BeautifulSoup(content, 'html.parser')

	containers = html_soup.find_all('pre')
	links = containers[0].findAll('a', href=True, text=True)
	link_list = []
	for link in links:
	    link_list.append(link['href'].replace('/', ''))
	    

	# currently available text datasets
	if input_date == 'check':
		available_month = sorted(set(link_list[1:-1]), reverse=True)
		print(available_month)
		return 0

	if len(input_date) == 6:
		input_date = input_date[:4]+'-'+input_date[4:]

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
	local_file = download_file(filename)
	print('Finished downloading: ', local_file, ' in Datasets folder')
	print('Now decompressing the file...')

	comp_file = gzip.open(local_file, 'rb')
	read_file = comp_file.read()
	comp_file.close()

	new_file_name = en_file.replace('.gz', '')
	f =  open(new_file_name, 'wb')
	f.write(read_file)
	f.close()

	shutil.move(new_file_name, 'Datasets/'+new_file_name)
	os.unlink(local_file)

	print('Finished decompressing the file.')

	return 0


def text(data_type, input_date, input_start, input_end):
	url = 'https://dumps.wikimedia.org/enwiki/'
	res = requests.get(url)
	content = str(res.text)
	html_soup = BeautifulSoup(content, 'html.parser')

	containers = html_soup.find_all('pre')
	links = containers[0].findAll('a', href=True, text=True)
	link_list = []
	for link in links:
	    link_list.append(link['href'].replace('/', '')[:6])
	    
	# currently available text datasets
	if input_date == 'available':
		available_month = sorted(set(link_list[1:-1]), reverse=True)
		print(available_month)
		return 0

	# default: the first dataset of the month as we'll update the dataset in monthly basis
	file_page = url+input_date+'01/'
	res_page = requests.get(file_page)
	content_page = str(res_page.text)
	html_page = BeautifulSoup(content_page, 'html.parser')

	container_link = html_page.find_all('li', class_='file')
	file_list = []
	for link in container_link:
	    if ('multistream' in link.text.split(' ')[0]) and ('.xml' in link.text.split(' ')[0]):
	        file_list.append(link.text.split(' ')[0])

	available_files = file_list[1:]

	# available number of files
	if input_end == 'check':
		print(len(available_files))
		return 0

	for files in available_files[int(input_start):int(input_end)]:
	    filename = file_page+files
	    local_file = download_file(filename)
	    print('Finished downloading: ', local_file, ' in Datasets folder')
	    print('Now decompressing the file...')

	    comp_file = bz2.BZ2File(local_file, 'rb')
	    read_file = comp_file.read()
	    comp_file.close()

	    new_file_name = '-'.join(local_file.split('-')[:-1])
	    f =  open(new_file_name, 'wb')
	    f.write(read_file)
	    f.close()

	    shutil.move(new_file_name, 'Datasets/'+new_file_name)
	    os.unlink(local_file)

	    print('Finished decompressing the file.')

	return 0


def checkCommand():
	print('Please check the available commands below:')
	print('python download_dataset.py text available month check')
	print('python download_dataset.py text (YYYYMM) number check')
	print('python download_dataset.py text (YYYYMM) (start_index) (end_index)')
	print('python download_dataset.py clickstream (YYYY-MM)')
	print('python download_dataset.py clickstream (YYYYMM)')
	print('python download_dataset.py clickstream check')

if __name__ == '__main__':
	try:
	    data_type = sys.argv[1]
	    input_date = sys.argv[2]

	    if data_type == 'clickstream':
	    	clickstream(data_type, input_date)
	    	# cmd to check available month: python download_dataset.py clickstream check
	    	# cmd to download data:  python download_dataset.py clickstream 202001 
	    	# 		 alternate cmd:  python download_dataset.py clickstream 2020-01 
	    elif data_type == 'text':
	    	input_start = sys.argv[3]
	    	input_end = sys.argv[4]
	    	text(data_type, input_date, input_start, input_end)
	    	# cmd to check available month: python download_dataset.py text available month check
	    	# cmd to check number of files in the month: python download_dataset.py text 202001 number check
	    	# cmd to download data:  python download_dataset.py text 202001 2 4

	except:
		checkCommand()

