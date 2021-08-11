import subprocess as sp
from scripts.trainer.utils import *

baseDirectory = "datasets"
data = baseDirectory + "/training.data"
cfg = baseDirectory + "/training.cfg"
model = baseDirectory + "/darknet53.conv.74"

#TODO: remove hardcoding to allow the use of different cfg files
def train(directory):
    generateTrainValidationTxtFile(directory)
    
    classes = directory.split("_")
    generateNamesFile("training.names", classes)
    generateDataFile(len(classes))

    maxBatches = 2000*len(classes)
    batches = "max_batches=" + str(maxBatches) + "\n"
    step1 = int(maxBatches * 0.8)
    step2 = int(maxBatches * 0.9)
    steps = "steps=" + str(step1) + "," + str(step2) + "\n"
    changeLine("training.cfg", 19, batches)
    changeLine("training.cfg", 21, steps)
    
    filters = "filters=" + str(3*(5+len(classes))) + "\n"
    changeLine("training.cfg", 602, filters)
    changeLine("training.cfg", 688, filters)
    changeLine("training.cfg", 775, filters)
    
    nClasses = "classes=" + str(len(classes)) + "\n"
    changeLine("training.cfg", 609, nClasses)
    changeLine("training.cfg", 695, nClasses)
    changeLine("training.cfg", 782, nClasses)

    #TODO: fix directories
    args = "./../darknet/darknet detector train " + data + " " + cfg + " " + model + " -dont_show -map > ./../datasets/output.log"
    process = sp.Popen(args, stdin=sp.PIPE, shell=True)
    
    return process