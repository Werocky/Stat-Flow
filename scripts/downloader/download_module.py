import os
import cv2

from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm

def download(df_val, folder, dataset_dir, class_name, class_code, limit = None, class_list=None, threads = 20):
    if os.name == 'posix':
        rows, columns = os.popen('stty size', 'r').read().split()
    elif os.name == 'nt':
        try:
            columns, rows = os.get_terminal_size(0)
        except OSError:
            columns, rows = os.get_terminal_size(1)
    else:
        columns = 50
    l = int((int(columns) - len(class_name))/2)

    print ('\n' + '-'*l + class_name + '-'*l)
    print('Downloading all the images.')

    images_list = df_val['ImageID'][df_val.LabelName == class_code].values
    images_list = set(images_list)
    print('[INFO] Found {} online images for {}.'.format(len(images_list), folder))

    if limit is not None:
        import itertools
        print('Limiting to {} images.'.format(limit))
        images_list = set(itertools.islice(images_list, limit))

    if class_list is not None:
        class_name_list = '_'.join(class_list)
    else:
        class_name_list = class_name
    print(class_name_list)
    download_img(folder, dataset_dir, class_name_list, images_list, threads)
    get_label(folder, dataset_dir, class_name, class_code, df_val, class_name_list)


def download_img(folder, dataset_dir, class_name, images_list, threads):
    image_dir = folder
    download_dir = os.path.join(dataset_dir, image_dir, class_name)
    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir)]
    images_list = list(set(images_list) - set(downloaded_images_list))

    pool = ThreadPool(threads)

    if len(images_list) > 0:
        print('Download of {} images in {}.'.format(len(images_list), folder))
        commands = []
        for image in images_list:
            path = image_dir + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
            command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path                    
            commands.append(command)

        list(tqdm(pool.imap(os.system, commands), total = len(commands) ))

        print('Done!')
        pool.close()
        pool.join()
    else:
        print('All images already downloaded.')


def get_label(folder, dataset_dir, class_name, class_code, df_val, class_list):
    print('Creating labels for {} of {}.'.format(class_name, folder))

    image_dir = folder
    if class_list is not None:
        download_dir = os.path.join(dataset_dir, image_dir, class_list)
        label_dir = os.path.join(dataset_dir, folder, class_list, 'Label')
    else:
        download_dir = os.path.join(dataset_dir, image_dir, class_name)
        label_dir = os.path.join(dataset_dir, folder, class_name, 'Label')

    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir) if f.endswith('.jpg')]
    images_label_list = list(set(downloaded_images_list))

    groups = df_val[(df_val.LabelName == class_code)].groupby(df_val.ImageID)
    for image in images_label_list:
        try:
            current_image_path = os.path.join(download_dir, image + '.jpg')
            dataset_image = cv2.imread(current_image_path)
            boxes = groups.get_group(image.split('.')[0])[['XMin', 'XMax', 'YMin', 'YMax']].values.tolist()
            file_name = str(image.split('.')[0]) + '.txt'
            file_path = os.path.join(label_dir, file_name)
            if os.path.isfile(file_path):
                f = open(file_path, 'a')
            else:
                f = open(file_path, 'w')

            for box in boxes:
                box[0] *= int(dataset_image.shape[1])
                box[1] *= int(dataset_image.shape[1])
                box[2] *= int(dataset_image.shape[0])
                box[3] *= int(dataset_image.shape[0])

                # each row in a file is name of the class_name, XMin, YMin, XMax, YMax (left top right bottom)
                print(class_name, box[0], box[2], box[1], box[3], file=f)

        except Exception as e:
            pass

    print('Labels creation completed.')
