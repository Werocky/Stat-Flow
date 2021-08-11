import os
import shutil

def mkdirs(dataset_folder, csv_folder, classes):
    directory_list = ['train', 'validation', 'test']
    for directory in directory_list:
        mainDirectory = os.path.join(dataset_folder, directory)
        if os.path.exists(mainDirectory):
            shutil.rmtree(mainDirectory)
        for class_name in classes:
            if not dataset_folder.endswith('_nl'):
                folder = os.path.join(dataset_folder, directory, class_name, 'Label')
            else:
                folder = os.path.join(dataset_folder, directory, class_name, 'Label')
            if not os.path.exists(folder):
                os.makedirs(folder)
            filelist = [f for f in os.listdir(folder) if f.endswith(".txt")]
            for f in filelist:
                os.remove(os.path.join(folder, f))

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

def progression_bar(total_images, index):
    rows, columns = os.popen('stty size', 'r').read().split()
    toolbar_width = int(columns) - 10
    image_index = index
    index = int(index / total_images * toolbar_width)

    print(' ' * (toolbar_width), end='\r')
    bar = "[{}{}] {}/{}".format('-' * index, ' ' * (toolbar_width - index), image_index, total_images)
    print(bar.rjust(int(columns)), end='\r')

mkdirs("datasets", "csv", ["Person", "Car"], "train")