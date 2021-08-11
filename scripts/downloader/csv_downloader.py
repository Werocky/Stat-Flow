import os
import sys
import time

import pandas as pd
import urllib.request

google_repo = 'https://storage.googleapis.com/openimages/2018_04/'

def TTV(csv_dir, name_file):
    CSV = os.path.join(csv_dir, name_file)
    error_csv(name_file, csv_dir)
    df_val = pd.read_csv(CSV)
    return df_val

def error_csv(file, csv_dir):
    if not os.path.isfile(os.path.join(csv_dir, file)):
        print("Missing the {} file.".format(os.path.basename(file)))
        print("Automatic download.")

        folder = str(os.path.basename(file)).split('-')[0]
        if folder != 'class':
            FILE_URL = str(google_repo + folder + '/' + file)
        else:
            FILE_URL = str(google_repo + file)

        FILE_PATH = os.path.join(csv_dir, file)
        save(FILE_URL, FILE_PATH)
        print('\n' + "File {} downloaded into {}.".format(file, FILE_PATH))

def save(url, filename):
    urllib.request.urlretrieve(url, filename, reporthook)

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * duration) + 1e-5))
    percent = int(count * block_size * 100 / (total_size + 1e-5))
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()