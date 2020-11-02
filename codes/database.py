import pymongo
from pymongo import MongoClient
import tabulate
import dataprocess

cluster = MongoClient(
    "mongodb+srv://NYPCLASSBOT:fatpeepee123@nyp-class-bot.boaao.mongodb.net/class-links?retryWrites=true&w=majority"
)
db = cluster["class-links"]


class Db:
    def __init__(self, guildId):
        self.__guildId = guildId
        self.__collection = db[self.__guildId]

        def delSelf(guildId):
            db.self.__collection.remove(guildId)

    def insertEntry(self, subj, day, time):
        post = {"day": day, "time": time, "subject": subj}
        self.__collection.insert_one(post)
        print("Entry is inserted.")
        return "Entry is inserted."

    def insertManyEntry(self, arrayOfPosts):
        db.self.__collection.insertMany(arrayOfPosts)
        print("Entries have been inserted.")

    # inserting multiple entry
    # post2 = {"_id": "subject", "time": 1200, "day:": "link"}
    # collection.insert_many([post, post2])

    def updateEntry(self, subj, day, time, newField, newValue):
        self.__collection.update_one(
            {"day": day, "time": time, "subject": subj},
            {"$set": {newField: newValue}},
        )
        print("Entry has been updated.")
        return "Entry has been updated "

    def deleteSingleEntry(self, subj, day, time):
        # show all entries for discord server
        # from the entry data, enter criterias for it to be deleted.
        self.__collection.delete_one(
            {
                "day": day,
                "time": time,
                "subject": subj,
            }
        )
        print("Entry has been deleted.")
        return "Entry has been deleted."
