import pymongo
from pymongo import MongoClient
import tabulate

cluster = MongoClient(
    "mongodb+srv://NYPCLASSBOT:fatpeepee123@nyp-class-bot.boaao.mongodb.net/class-links?retryWrites=true&w=majority"
)
db = cluster["class-links"]
collection = db["timing-links"]

def insertEntry(guildId, subj, lessonType, day, time):
    post = {'guildId': guildId,'subject':subj,  'lessonType': lessonType, 'day': day, 'time':time}
    collection.insert_one(post)
    print('Entry is inserted.')

# inserting multiple entry
# post2 = {"_id": "subject", "time": 1200, "day:": "link"}
# collection.insert_many([post, post2])

def findEntry(guildId):
    try:
        results = collection.find({"guildId": guildId})
        header = results[1].keys()
        rows = [x.values() for x in results]
    except IOError:
        return "Error! Id does not exists in database."
    return tabulate.tabulate(rows, header, tablefmt='rst')
        

def updateEntry(guildId, subject, newField, newValue):
    print(findEntry(guildId))
    collection.update_one({"guildId":guildId, "subj":subject}, {"$set":{newField:newValue}})
    

def countEntry():
    return collection.count_documents({})


def deleteEntry(guildId):
    collection.delete_one({"guildId":guildId})
    return('Entry has been deleted.')
#insertEntry('1234', 'human', 1, 1200)
#updateEntry("123456", "poopoo", "subj", "benis")