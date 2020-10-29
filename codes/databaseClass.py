import pymongo
from pymongo import MongoClient
import tabulate

cluster = MongoClient(
    "mongodb+srv://NYPCLASSBOT:fatpeepee123@nyp-class-bot.boaao.mongodb.net/class-links?retryWrites=true&w=majority"
)
db = cluster["class-links"]
collection = db["timing-links"]

class database:
    def __init__(self, guildId):
        self.__id = guildId

    def insertEntry(self, subj, lessonType, day, time):
        post = {'guildId': self.__id,'subject':subj,  'lessonType': lessonType, 'day': day, 'time':time}
        collection.insert_one(post)
        print('Entry is inserted.')

    #def insertMultiEntry(self):
    # inserting multiple entry
    # post2 = {"_id": "subject", "time": 1200, "day:": "link"}
    # collection.insert_many([post, post2])

    def displayEntry(self):
        try:
            results = collection.find({"guildId": self.__id})
            header = results[1].keys()
            rows = [x.values() for x in results]
        except IOError:
            return "Error! Id does not exists in database."
        return tabulate.tabulate(rows, header, tablefmt='rst')
            

    def updateEntry(self, subject, newField, newValue):
        print(displayEntry(self.__id))
        collection.update_one({"guildId":self.__id, "subj":subject}, {"$set":{newField:newValue}})
        

    def countEntry(self):
        return len(collection.find({"guildId": self.__id}))


    def deleteEntry(self):
        collection.delete_one({"guildId":self.__id})
        return('Entry has been deleted.')
#insertEntry('1234', 'human', 1, 1200)
#updateEntry("123456", "poopoo", "subj", "benis")