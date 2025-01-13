class Quabo:

    def __init__(self, address, data):

        self.address = address
        self.data = data

class Packet:

    def __init__(self, source_ip, timestamp, data, length):#, number):

        self.source_ip = source_ip
        self.timestamp = timestamp
        self.data = data
        self.length = length
        #self.number = number

class Telescope:

    def __init__(self, name, dome, quabo_addresses, data):

        self.name = name
        self.dome = dome
        self.quabo_addresses = quabo_addresses
        self.data = data

class Image:

    def __init__(self, data, timestamp, number):

        self.data = data
        self.timestamp = timestamp
        self.number = number

class Sequence:

    def __init__(self, sequence, median_data, telescope, file_name):

        self.sequence = sequence
        self.median_data = median_data
        self.telescope = telescope
        self.file_name = file_name

class Median:
    def __init__(self, median_frame, frame_selection):
        
        self.median_frame = median_frame
        self.frame_selection = frame_selection

#class Source_Candidate(self):
#
#    def __init__():
#        self.

class Source:

    def __init__(self,
                 identifier,
                 first_detection_time_ms,
                 last_detection_time_ms,
                 motion_history,
                 average_proper_motion,
                 proper_motion_direction):

        self.identifier = identifier
        self.first_detection_time = first_detection_time_ms
        self.last_detection_time = last_detection_time_ms
        self.motion_history = motion_history
        self.average_proper_motion = average_proper_motion
        self.proper_motion_direction = proper_motion_direction