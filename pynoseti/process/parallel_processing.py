from multiprocessing import Pool
from tqdm import tqdm


def parallel_processing(data, function, available_threads):

    allowed_threads = int(available_threads/2)

    with Pool(allowed_threads) as pool:

        results = list(tqdm(pool.imap(function, data), total=len(data)))#, desc=f'Processing file {file_iterate} of {file_count}...'))

    return results