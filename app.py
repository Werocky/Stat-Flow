import json

from multiprocessing import Process
from flask import Flask, render_template, request, redirect, flash
from scripts.downloader.img_downloader import downloader
from scripts.trainer.trainer import train
from scripts.trainer.utils import generateNamesFile, plotTrainLoss
from scripts.db.dbManager import *
from scripts.db.calcUtils import *
from scripts.configuration.configure import *

app = Flask(__name__)
app.secret_key = "my web app secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/opendatacam"
isTraining = False
isDownloading = False
#disable caching, required to have dynamic matplotlib plots
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
output_code = ''
downloadProcess = Process()
trainProcess = Process()


@app.route('/')
def index():
    return render_template('index.html', page = 'home')

@app.route("/training")
def training():
    global isTraining
    if isTraining:
        return render_template('training_statistics.html', output = output_code, page = 'training', trainloss=plotTrainLoss)
    else:
        return render_template('training.html', page = 'training')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html', page = 'statistics', plotGr=plotGrafic, plotHi=plotHistogram)

@app.route("/configure")
def configure():
    return render_template('configure.html', page = 'configure')

@app.route("/configureODC", methods = ['POST'])
def configureODC():
    config = {}
    config['yoloPath']= request.form.get('yoloPath')
    config['video_input']= request.form.get('video_input')
    config['data']= request.form.get('data')
    config['cfg']= request.form.get('cfg')
    config['weights']= request.form.get('weights')
    operationResult = configureFile(config)
    if operationResult:
        flash("Config File updated succesfully")
    else:
        flash("Errors occurred during File update, please try again")
    return redirect("configure")

#redirect to external websites, in case it is required
@app.route('/<string:variable>',)
def go_outside_flask_method(variable):
    if not ("http://" in variable or "https://" in variable):
        variable = 'https://' + variable
    return redirect(variable, code = 307) 

#processes the data for new training
@app.route('/get_post_json', methods=['POST'])
def get_post_json():
    global output_code   
    data = request.get_json()

    output_code = "data recieved: Starting to process data.\n\n"
    
    dictToStr = json.dumps(data)
    dictToStr = str(dictToStr)
    dictToStr.replace("'", '"')

    new_data= json.loads(dictToStr)

    new_values = []

    #TODO: fix implementation
    for value in new_data.values():
        new_values.append(value)

    classes = []
    quantity = []
    for x in range(0, len(value), 2):
        classes.append(value[x])
        quantity.append(value[x+1])
    #
    output_code = "data processed: starting dataset download for training(operation can take some time).\n\n"
    
    global isTraining, isDownloading, downloadProcess, trainProcess
    isTraining = isDownloading = True
    classString = [value.replace('_', ' ') for value in classes]
    downloadProcess = Process(target= downloader, args= (classString, quantity))
    downloadProcess.start()
    downloadProcess.join()
    isDownloading = False

    output_code = "data downloaded: dataset downloaded, model training in progress.\n\n"

    multiclass_name = ['_'.join(classString)]
    generateNamesFile("datasets/training.txt", classes)
    trainProcess = train(multiclass_name[0])
    trainProcess.wait()
    isTraining = False
    output_code = "model trained: model has been trained, exiting training mode.\n\n"

    return

#TODO: improve performances when pulling data from db
def getData():
    global app
    db = connectToDb(app)
    newData=[]
    for i in range(0, 7):
        data = pullDailyTracking(db, i)
        newData.append(calculateTraffic(data))
    return newData

def plotGrafic():
    data = getData()
    directory = graphic(data)
    return directory

def plotHistogram():
    data = getData()
    directory = histogram(data)
    return directory

if __name__ == "__main__":
    app.run(debug=True)