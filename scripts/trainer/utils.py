import os
import sys
import matplotlib.pyplot as plt
from configparser import SafeConfigParser

def generateTrainValidationTxtFile(directory):
    image_files = []
    os.chdir(os.path.join("datasets/train", directory))
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".jpg"):
            image_files.append("datasets/train/"+ directory + "/" + filename)
    os.chdir("..")
    with open("train.txt", "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()
    os.chdir("../..")


    image_files = []
    os.chdir(os.path.join("datasets/validation", directory))
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".jpg"):
            image_files.append("datasets/validation/" + directory + "/" + filename)
    os.chdir("..")
    with open("valid.txt", "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()
    os.chdir("..")

def generateNamesFile(filename, names):
    with open(filename, 'w') as f:
        for name in names:
            f.write(name)
            f.write('\n')

def generateDataFile(classes):
    with open("training.data", "w") as f:
        f.write(str(classes))
        f.write('\n')
        f.write("train = datasets/train/train.txt \n")
        f.write("valid = datasets/validation/valid.txt \n")
        f.write("names = datasets/training.names \n")
        f.write("backup = datasets/backup/ \n")

def changeLine(file, line, value):
    a_file = open(file, "r")
    list_of_lines = a_file.readlines()

    list_of_lines[line] = value

    a_file = open(file, "w")
    a_file.writelines(list_of_lines)
    a_file.close()

def plotTrainLoss(logfile):
    directory = './static/plots/training_loss_plot.png'
    lines = []
    for line in open(logfile, "r"):
        if "avg" in line:
            lines.append(line)

    iterations = []
    avg_loss = []
    print('Retrieving data and plotting training loss graph...')
    for i in range(len(lines)):
        lineParts = lines[i].split(',')
        iterations.append(int(lineParts[0].split(':')[0]))
        avg_loss.append(float(lineParts[1].split()[0]))

    fig = plt.figure()
    for i in range(0, len(lines)):
        plt.plot(iterations[i:i+2], avg_loss[i:i+2], 'r.-')

    plt.xlabel('Epochs')
    plt.ylabel('Avg Loss')
    fig.savefig(directory, dpi=100)

    print('Done! Plot saved as training_loss_plot.png')

    return directory