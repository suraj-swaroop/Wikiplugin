import requests
import shutil
import gzip
import bz2
import os
import re
import sys
from bs4 import BeautifulSoup


# Create a file path
def checkDirectory(filePath):
    try:
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print("[Success] Creating a directory: ", filePath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("[Error] Failed creating a directory")
            raise

            
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

    link_list = []
    print("\n************** clickstream **************")
    for link in links:
        link_list.append(link['href'].replace('/', ''))

    # currently available text datasets
    months = sorted(set(link_list[1:-1]), reverse=True)
    print(months)
    
    for month in months:
        month = month.replace("-", "")
        filePath = '../working/clickstream/wikipedia_clickstream_' + month + '.txt'
        with open(filePath, 'w+') as tx_file:
            tx_file.write("")
            
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

    print("************** text **************")
    for month in available_month:
        # default: the first dataset of the month as we'll update the dataset in monthly basis
        file_page = url+month+'01/'  # ex) /20200201/, /20200101/
        res_page = requests.get(file_page)
        content_page = str(res_page.text)
        html_page = BeautifulSoup(content_page, 'html.parser')
        container_link = html_page.find_all('li', class_='file')
        
        file_list = []
        for link in container_link:
            if ('multistream' in link.text.split(' ')[0]) and ('.xml' in link.text.split(' ')[0]):
                file_list.append(link.text.split(' ')[0])

        available_files = file_list[1:]
        
        filePath = '../working/text/wikipedia_text_' + month + '.txt'
        # Write the months into 'wikipedia_text.txt'
        with open(filePath,'w+') as tx_file:
            for file in available_files:
                tx_file.write("%s\n" % file)

        print("Downloadable Month: {}, Numbers: {}".format(month, len(available_files)))
    # End of for loop

    return 0


############################################################################
# Name : pageview
# Purpose : Checking downloadable months
# Input : NULL
# Return : 0
############################################################################            
def pageview():
    url = 'http://dumps.wikimedia.your.org/other/pageviews/2020/'
    res = requests.get(url)
    content = str(res.text)
    html_soup = BeautifulSoup(content, 'html.parser')
    
    links = [a['href'] for a in html_soup.find_all('a', href=True)]
    if links[0] == '../':
        links.remove('../')

    available_month = []
    for link in links:
        available_month.append(link.replace('/', ''))

    print("\n************** Pageview **************")
    for month in available_month:
        # default: the first dataset of the month as we'll update the dataset in monthly basis
        file_page = url+month+'/'
        res_page = requests.get(file_page)
        content_page = str(res_page.text)
        html_page = BeautifulSoup(content_page, 'html.parser')
        
        container_link = [a['href'] for a in html_page.find_all('a', href=True)]     
        available_files = container_link[1:]

        # available number of files
        month = month.replace("-", "")
        
        filePath = '../working/pageview/wikipedia_pageview_' + month + '.txt'
        # Write the months into 'wikipedia_text.txt'
        with open(filePath,'w+') as tx_file:
            for file in available_files:
                tx_file.write("%s\n" % file)
                
        print("Downloadable Month: {}, Numbers: {}".format(month, len(available_files)))
    # End of for loop  

    return 0


if __name__ == '__main__':
    # Wikipedia download datasets
    wk_dataset = ['text', 'clickstream', 'pageview']

    for data_type in wk_dataset:
        if data_type == 'text': 
            filePath = '../working/' + data_type
            checkDirectory(filePath)
            text()
        elif data_type == 'clickstream':
            filePath = '../working/' + data_type
            checkDirectory(filePath)
            clickstream()
        elif data_type == 'pageview':
            filePath = '../working/' + data_type
            checkDirectory(filePath)
            pageview()
    # End of for loop
   
