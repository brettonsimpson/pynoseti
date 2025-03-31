from datetime import datetime

def convert_unix_time(time, milliseconds=True):

    date_object = datetime.fromtimestamp(time/10e2)

    if milliseconds is True:

        output = date_object.strftime('%Y-%m-%d %H:%M:%S') +':'+ str(date_object.microsecond)
    
    else:
        output = date_object.strftime('%Y-%m-%d %H:%M:%S')

    return output