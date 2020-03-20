import requests
import shutil
import gzip
import bz2
import os
import re
import sys
from bs4 import BeautifulSoup


############################################################################
# Name : clickstream
# Purpose : Checking downloadable months
# Input : NULL
# Return : 0
############################################################################
def clickstream():
    url = 'https://dumps.wikimedia.org/other/clickstream/'
    res = requests.get(url)
    content = str(res.text)
    html_soup = BeautifulSoup(content, 'html.parser')

    containers = html_soup.find_all('pre')
    links = containers[0].findAll('a', href=True, text=True)
    replaced_link_list = []
    link_list = []
    for link in links:
        link_list.append(link['href'].replace('/', ''))

    # currently available text datasets
    months = sorted(set(link_list[1:-1]), reverse=True)
    
    print(months)
    
    # Write the months into 'wikipedia_clickstream.txt'
    with open('wikipedia_clickstream.txt','w+') as cs_file:
        for month in months:
            cs_file.write("%s\n" % (month.replace('-', '')))

#     clickstream_dictionary = {}
#     for month in months:
#         # default: the first dataset of the month as we'll update the dataset in monthly basis
#         available_files = []
#         file_page = url+month+'/'
#         res_page = requests.get(file_page)        
#         content_page = str(res_page.text)
#         html_page = BeautifulSoup(content_page, 'html.parser')
        
#         for a in html_page.find_all('a', href=True):
#             available_files.append(a['href'])

#         # available number of files
#         clickstream_dictionary.update( {month : len(available_files)} )
#         print("Downloadable Month: {}, Numbers: {}".format(month, len(available_files)))
#     # End of for loop

#     # Write the months into 'wikipedia_clickstream.txt'
#     with open('wikipedia_clickstream.txt','w+') as cs_file:
#         for month in sorted (clickstream_dictionary.keys(), reverse=True):
#             cs_file.write("%s:%s\n" % (month.replace('-', ''), clickstream_dictionary[month]))
            
    return 0


############################################################################
# Name : text
# Purpose : Checking downloadable months counts and the number of files
# Input : NULL
# Return : 0
############################################################################
def text():
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
    available_month = sorted(set(link_list[1:-1]), reverse=True)

    text_dictionary = {}
    for month in available_month:
        # default: the first dataset of the month as we'll update the dataset in monthly basis
        file_page = url+month+'01/'
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
        text_dictionary.update( {month : len(available_files)} )
        print("Downloadable Month: {}, Numbers: {}".format(month, len(available_files)))
    # End of for loop

    # Write the months into 'wikipedia_text.txt'
    with open('wikipedia_text.txt','w+') as tx_file:
        for month in sorted (text_dictionary.keys(), reverse=True):
            tx_file.write("%s:%s\n" % (month, text_dictionary[month]))
            
    return 0


if __name__ == '__main__':
    # Wikipedia download datasets
    wk_dataset = ['text', 'clickstream']
    
    for data_type in wk_dataset:
        if data_type == 'text':    
            text()
        elif data_type == 'clickstream':
            clickstream()
    # End of for loop
   