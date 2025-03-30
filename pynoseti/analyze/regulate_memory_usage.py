import resource
import psutil

def cap_memory_usage(cap):

    soft, hard = resource.getrlimit(resource.RLIMIT_AS) 

    resource.setrlimit(resource.RLIMIT_AS, (cap, hard))



def get_memory_usage(): 

    process = psutil.Process()

    usage = process.memory_info().rss

    return usage/10e9