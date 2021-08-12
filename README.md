# Introduction
This project has been created to simplify the monitoring of different flows (traffic, people, etc.). It is possible to create a custom model for different scenarios training a new model from scratch. It is supposed to run on a Jetson board.  
The project is still in an early state and could have some bugs.

# Requirements
Jetson board to host the platform.  
OpenDataCam (https://github.com/opendatacam/opendatacam) is required since it has been used on the main page to do the detections and data collection.  
YOLO Darknet (https://pjreddie.com/darknet/yolo/) is required to start training a new model from scratch.  

# Installation
To start using the software it is required to upload the source code on the jetson board and run the app.py file.  
```
$ git clone https://github.com/Werocky/Stat-Flow
$ cd Stat-Flow
$ pip install -r requirements.txt
$ python app.py
```


# TODOs
- [ ] add dropdown menu for classes selection in the training page  
- [ ] improve information visualizzation during the training process  
- [ ] add training controls  
- [ ] pull data automatically every hour  
- [ ] schedule ODC recordings  
- [ ] improve configuration page  
   
- [ ] code clueanup  
