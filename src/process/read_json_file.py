import json
from functions import Telescope

def read_json_file():

    with open('config.json', 'r') as file:
        
        config = json.load(file)

    telescope_list = []

    quabo_address_list = []

    for setting in config['telescopes']:

        telescope = Telescope(name = setting['identifier'],
                            dome = setting['dome'], 
                            quabo_addresses = setting['quabo_addresses'],
                            data = []
                            )
        
        telescope_list.append(telescope)

        for address in telescope.quabo_addresses:

            if address not in quabo_address_list:

                quabo_address_list.append(address)
    
    return telescope_list, quabo_address_list