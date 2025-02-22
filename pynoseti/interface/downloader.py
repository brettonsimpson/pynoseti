import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3

def downloader(url, target_directory):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with open('config.json', 'r') as file:
        config = json.load(file)
        username = config['credentials'][0]['username']
        password = config['credentials'][0]['username']

    print(f'\nIndexing data from {url}\n')

    directory = BeautifulSoup(requests.get(url, auth=(username, password), verify=False).text, features='html.parser')

    file_list = directory.find_all('a')

    for entry in tqdm(file_list):

        filename = ''

        address = entry.get('href')

        response = requests.get(address, auth=(username, password), verify=False)

        for char in reversed(address):
            if char == '/':
                break

            filename = char + filename
        
        if '.pcapng' in filename:

            with open(f'{target_directory}/{filename}', 'wb') as file:

                file.write(response.content)

    return len(file_list)

