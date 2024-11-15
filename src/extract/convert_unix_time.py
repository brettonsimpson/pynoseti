import datetime

def convert_unix_time(time):
    #

    date_object = datetime.fromtimestamp(time)
    #

    output = date_object.strftime('%Y-%m-%d %H:%M:%S') +':'+ str(date_object.microsecond)
    #

    return output