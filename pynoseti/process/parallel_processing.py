from multiprocessing import Pool
from tqdm import tqdm


def parallel_processing(data, function, available_threads):

    allowed_threads = int(3*available_threads/4)

    with Pool(allowed_threads) as pool:

        results = list(tqdm(pool.imap(function, data), total=len(data)))#, desc=f'Processing file {file_iterate} of {file_count}...'))

    return results