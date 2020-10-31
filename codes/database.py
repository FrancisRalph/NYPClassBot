import pymongo
from pymongo import MongoClient
import tabulate

cluster = MongoClient(
    "mongodb+srv://NYPCLASSBOT:fatpeepee123@nyp-class-bot.boaao.mongodb.net/class-links?retryWrites=true&w=majority"
)
db = cluster["class-links"]
collection = db["timing-links"]


def insertEntry(guildId, subj, lessonType, day, time):
    post = {
        "guildId": guildId,
        "subject": subj,
        "lessonType": lessonType,
        "day": day,
        "time": time,
    }
    collection.insert_one(post)
    print("Entry is inserted.")
    return "Entry is inserted."


# inserting multiple entry
# post2 = {"_id": "subject", "time": 1200, "day:": "link"}
# collection.insert_many([post, post2])


def findEntry(guildId):
    try:
        results = collection.find({"guildId": guildId})
        header = results[1].keys()
        rows = [x.values() for x in results]
    except IOError:
        print("Error! Id does not exists in database.")
        return "Error! Id does not exists in database."
    print("Table is shown.")
    return tabulate.tabulate(rows, header, tablefmt="rst")


def updateEntry(guildId, subject, day, newField, newValue):
    print(findEntry(guildId))
    collection.update_one(
        {"guildId": guildId, "subject": subject, "day": day},
        {"$set": {newField: newValue}},
    )
    print("Entry has been updated.")
    return "Entry has been updated "


def countEntry():
    return collection.count_documents({})


def deleteEntry(guildId, subj, lessonType, day, time):
    # show all entries for discord server
    findEntry(guildId)
    # from the entry data, enter criterias for it to be deleted.
    collection.delete_one(
        {
            "guildId": guildId,
            "subject": subj,
            "lessonType": lessonType,
            "day": day,
            "time": time,
        }
    )
    print("Entry has been deleted.")
    return "Entry has been deleted."


# insertEntry('1234', 'human', 1, 1200)
# updateEntry("123456", "poopoo", "subj", "benis")
