import json

def readConfigFile():
    with open('config.json') as json_file:
        data = json.load(json_file)
    return data

def writeConfiguration(data):
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)

def configureFile(data):
    try:
        configFile = readConfigFile()
        configFile['PATH_TO_YOLO_DARKNET'] = data['yoloPath']
        configFile['VIDEO_INPUT'] = data['video_input']
        configFile['NEURAL_NETWORK_PARAMS']['yolov4-tiny']['data'] = data['data']
        configFile['NEURAL_NETWORK_PARAMS']['yolov4-tiny']['cfg'] = data['cfg']
        configFile['NEURAL_NETWORK_PARAMS']['yolov4-tiny']['weights'] = data['weights']
        writeConfiguration(configFile)
        return True
    except:
        return False