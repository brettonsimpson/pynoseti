import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from tqdm import tqdm

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('config.json', 'r') as file:
    config = json.load(file)
    username = config['credentials'][0]['username']
    password = config['credentials'][0]['username']

url = input('Please enter a URL from which you would like to download PANOSETI data from: ')
url = 'https://132.239.146.24/~jmaire/panoseti/DATA/20221118/20221118.html'

print(f'Indexing data from {url}\n')

directory = BeautifulSoup(requests.get(url, auth=(username, password), verify=False).text, features='html.parser')

file_list = directory.find_all('a')

#exit()
#for element in directory:
#    file_list.append(element)
    

#for element in file_list:
#    print(f'{element}\n')

#for link in file_list:
#    if '.pcapng' in link.get('href'):
#        with open(link, 'wb') as file:
#            file.write(file)

'''
address = file_list[28].get('href')

print(f'\n{address}\n')

response = requests.get(address, auth=(username, password), verify=False)

filename = ''

for char in reversed(address):
    if char == '/':
        break

    filename = char + filename

with open(f'/Users/brettonsimpson/Desktop/Web_scraping_test/{filename}', 'wb') as file:

    file.write(response.content)

print('Success!')
'''

for entry in tqdm(file_list):

    filename = ''

    address = entry.get('href')

    response = requests.get(address, auth=(username, password), verify=False)

    for char in reversed(address):
        if char == '/':
            break

        filename = char + filename    

    
    if '.pcapng' in filename:

        with open(f'/Users/brettonsimpson/Desktop/Web_scraping_test/{filename}', 'wb') as file:

            file.write(response.content)





