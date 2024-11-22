from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def parallel_processing(data, function, threads, file_count, file_iterate):

    #threads = int(cpu_count()/4)


    with Pool(threads) as pool:

        results = list(tqdm(pool.imap(function, data), total=len(data)))#, desc=f'Processing file {file_iterate} of {file_count}...'))

    return results