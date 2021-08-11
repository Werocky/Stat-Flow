import os
import pandas as pd

from .csv_downloader import *
from .download_module import *
from .utils import *
from .annotation_converter import convert_annotations

def downloader(classes, limit):
    dataset_dir = "../datasets"
    csv_dir = "../" + dataset_dir + "/csv"

    name_file_class = 'class-descriptions-boxable.csv'
    CLASSES_CSV = os.path.join(csv_dir, name_file_class)

    folders = ['train', 'validation', 'test']
    file_list = ['train-annotations-bbox.csv', 'validation-annotations-bbox.csv', 'test-annotations-bbox.csv']

    print('Downloading {} together.'.format(classes))
    
    multiclass_name = ['_'.join(classes)]
    mkdirs(dataset_dir, csv_dir, multiclass_name)
    error_csv(name_file_class, csv_dir)
    df_classes = pd.read_csv(CLASSES_CSV, header=None)
    
    class_dict = {}
    for class_name in classes:
	    class_dict[class_name] = df_classes.loc[df_classes[1] == class_name].values[0][0]

    x = 0
    for class_name in classes:   
        for i in range(3):
            name_file = file_list[i]
            df_val = TTV(csv_dir, name_file)
            download(df_val, folders[i], dataset_dir, class_name, class_dict[class_name], int(limit[x]), classes, 4)
        x += 1
    convert_annotations()