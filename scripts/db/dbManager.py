from flask_pymongo import PyMongo
import datetime, json
from datetime import timedelta

def connectToDb(app):
    client = PyMongo(app)
    return client.db

#debug
def printEverything(db):
    results = db.tracker.find()
    for result in results:
        print(result)

def pullDailyTracking(db, chosenDay):
    from_date = to_date = datetime.datetime.now().replace(day= datetime.today() - timedelta(days=chosenDay) , hour=0, minute=0, second=0)
    to_date = to_date.replace(day= datetime.today() + timedelta(days= 1))
    results = db.recordings.find({
        'dateStart': {
            "$gte": from_date,
            "$lt": to_date
        },
        'dateEnd': {
            "$gte": from_date,
            "$lt": to_date
        }

    }, { 'counterSummary':1, 'trackerSummary':1 })

    #TODO: add proper error handling
    values = []
    for result in results:
        del result['_id']
        for key in result.keys():
            values.append(json.dumps(result[key]))

    for elem in values:
        try:
            newData = json.loads(elem)
        except IndexError:
            newData = 0
    return newData