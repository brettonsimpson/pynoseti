def reader_function():
    
    import pcapng
    from pcapng import FileScanner
    from pcapng.blocks import EnhancedPacket
    import os
    import time
    import json
    import progressbar

    print("\n")
    #path = input('Please specify the location of your Wireshark capture file: ')

    # Declares the list that will hold the hexadecimal data for each packet.

    ###########################################################
    path = "C:/Pause_onskyph0pe_ima0pe__20230426_044904.pcapng"
    #path = "/home/brett/Data_for_pynoseti/Pause_onskyph0pe_ima0pe__20230426_040905.pcapng"
    # Specifies the path to the file to be used in processing.
    # Don't forget to change when using a new file.
    ###########################################################

    packet_list = []
    # Declares the list that will hold the hexadecimal data for each packet.



    import datetime
    print("Reading selected file...")
    print("\n")

    with open(path, 'rb') as file:
        scanner = FileScanner(file)
        for block in scanner:
            if isinstance(block, pcapng.blocks.EnhancedPacket):
                # Checks, while iterating over each block, if it is of the EnchancedPacket data type. If so,
                # its hexadecimal packet data is stored in 'packet_array'.
                packet = block.packet_data
                hex_data = packet.hex()
                packet_list.append(hex_data)

    class Packet:
        def __init__(self, number, source_ip, data):
            self.number = number
            self.source_ip = source_ip
            self.data = data 

    

    i=0
    packet_array = []
    bar = progressbar.ProgressBar(max_value=len(packet_list))
    for packet in packet_list:
        packet_array.append(Packet(i+1, get_image_source_ip(packet), row_splitter(packet)))
        i+=1
        bar.update(i)

    packet_array = np.array(packet_array)

    class Quabo:
        def __init__(self, address, data):
            self.address = address
            self.data = data

    class Telescope:
        def __init__(self, name, dome, quabo_addresses, quabo_array, data):
            self.name = name
            self.dome = dome
            self.quabo_addresses = quabo_addresses
            self.quabo_array = quabo_array
            self.data = data

    with open('config.json', 'r') as file:
        config = json.load(file)
    telescope_list = []
    quabo_address_list = []
    for setting in config['telescopes']:
        telescope = Telescope(name = setting['identifier'],
                            dome = setting['dome'], 
                            quabo_addresses = setting['quabo_addresses'],
                            quabo_array = [],
                            data = []
                            )
        telescope_list.append(telescope)
        for address in telescope.quabo_addresses:
            if address not in quabo_address_list:
                quabo_address_list.append(address)

    print("\nConverting hexidecimal data to photon intensity...\n")
    print('Recognized telescopes:', '\n')

    i=1
    for telescope in telescope_list:
        print(str(i)+': '+telescope.name)
        i+=1
    telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')

    if telescope_choice != '':

        telescope_choice = int(telescope_choice)-1
        for packet in packet_array:
            if packet.source_ip in telescope_list[telescope_choice].quabo_addresses:
                telescope_list[telescope_choice].data.append(packet)

        processed_packet_list = [[], [], [], []]
        for packet in telescope_list[telescope_choice].data:
            if packet.source_ip == telescope_list[telescope_choice].quabo_addresses[0]:
                processed_packet_list[0].append(packet)

            elif packet.source_ip == telescope_list[telescope_choice].quabo_addresses[1]:
                processed_packet_list[1].append(packet)

            elif packet.source_ip == telescope_list[telescope_choice].quabo_addresses[2]:
                processed_packet_list[2].append(packet)
    
            elif packet.source_ip == telescope_list[telescope_choice].quabo_addresses[3]:
                processed_packet_list[3].append(packet)


        board_frame_count = [len(processed_packet_list[0]), len(processed_packet_list[1]), len(processed_packet_list[2]), len(processed_packet_list[3])]

        i=0
        image_list = []
        image_median = np.median(quabo_image_compiler((processed_packet_list[0])[int(np.min(board_frame_count)/2)].data,
                                                    (processed_packet_list[1])[int(np.min(board_frame_count)/2)].data,
                                                    (processed_packet_list[2])[int(np.min(board_frame_count)/2)].data,
                                                    (processed_packet_list[3])[int(np.min(board_frame_count)/2)].data))
        for element in range(np.min(board_frame_count)):
            image_list.append(quabo_image_compiler((processed_packet_list[0])[i].data,
                                                    (processed_packet_list[1])[i].data,
                                                    (processed_packet_list[2])[i].data,
                                                    (processed_packet_list[3])[i].data)-image_median)
            i+=1
        return np.array(image_list)