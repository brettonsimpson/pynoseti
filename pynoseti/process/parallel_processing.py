from multiprocessing import Pool
from tqdm import tqdm


def parallel_processing(data, function, allowed_threads):
    
    with Pool(allowed_threads) as pool:

        try:
            results = list(tqdm(pool.imap(function, data), total=len(data)))#, desc=f'Processing file {file_iterate} of {file_count}...'))

        except UnboundLocalError as e:
            print('\nUnbound local error encountered. Continuing to next file.\n')

    return results