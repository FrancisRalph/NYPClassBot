import pymongo
from pymongo import MongoClient
import tabulate
import datetime
from difflib import SequenceMatcher

cluster = MongoClient(
    "mongodb+srv://NYPCLASSBOT:fatpeepee123@nyp-class-bot.boaao.mongodb.net/class-links?retryWrites=true&w=majority"
)
db = cluster["class_links"]

def get_similarity(a, b):
    return SequenceMatcher(
        None, a, b
    ).ratio()

class Db:
    cluster = db

    def __init__(self, guildId):
        self.guildId = guildId
        # self.collection = db[str(guildId)]
        self.collection = db[guildId]
        # Remove this^^ after creation of cluster from timetable is created

    def delSelf(self):
        db.self.collection.remove(self.guildId)

    def insertEntry(self, subj, day, time):
        post = {"day": day, "time": time, "subject": subj}
        self.collection.insert_one(post)
        print("Entry is inserted.")
        return "Entry is inserted."

    def insertManyEntry(self, arrayOfPosts):
        self.collection.insert_many(arrayOfPosts)
        print("Entries have been inserted.")

    # inserting multiple entry
    # post2 = {"_id": "subject", "time": 1200, "day:": "link"}
    # collection.insert_many([post, post2])

    def updateEntry(self, subj, day, time, newField, newValue):
        self.collection.update_one(
            {"day": day, "time": time, "subject": subj},
            {"$set": {newField: newValue}},
        )
        print("Entry has been updated.")
        return "Entry has been updated "

    def findEntry(self, subj, day, time):
        x = self.collection.find({"day": day, "time": time, "subject": subj})
        return x

    def deleteSingleEntry(self, subj, day, time):
        # show all entries for discord server
        # from the entry data, enter criterias for it to be deleted.
        self.collection.delete_one(
            {
                "day": day,
                "time": time,
                "subject": subj,
            }
        )
        print("Entry has been deleted.")
        return "Entry has been deleted."

    def getAllEntry(self):
        entries = []
        x = self.collection.find()
        for i in x:
            entries.append(i)
        return entries

    def getEntriesMergedBySubject(self):
        entries = self.getAllEntry()

        sorted_entries = sorted(
            entries, key=lambda _entry: (_entry["day"], _entry["time"])
        )

        cleaned_entries = []
        for entry in sorted_entries:
            already_cleaned = False
            for cleaned_entry in cleaned_entries:
                if cleaned_entry["day"] == entry["day"]:
                    similarity = get_similarity(entry["subject"], cleaned_entry["subject"])
                    if similarity > 0.7:
                        already_cleaned = True
                        cleaned_entry["endEntry"] = entry.copy()

                        cleaned_link = cleaned_entry.get("link")
                        current_link = entry.get("link")
                        if cleaned_link is None and current_link is not None:
                            cleaned_entry.set("link", current_link)
                        break
            if cleaned_entries.count(entry) == 0 and not already_cleaned:
                cleaned_entries.append(entry)

        return cleaned_entries

    def getMergedSubjectEntryFromDay(self, day: int, subject: str, threshold=0.7):
        merged_entries = self.getEntriesMergedBySubject()
        similar = []
        for entry in merged_entries:
            if entry["day"] == day:
                similarity = get_similarity(entry["subject"], subject)
                if similarity > threshold:
                    similar.append(
                        {
                            "similarity": similarity,
                            "entry": entry
                        }
                    )

        if len(similar) > 0:
            return sorted(similar, key=lambda x: x["similarity"])[-1]["entry"]


if __name__ == "__main__":
    # 769097949514563594
    guildDb = Db("769097949514563594_cip")
    # print(list(db.list_collection_names()))
    print(sorted(guildDb.getAllEntry(), key=lambda entry: (entry["day"], entry["time"])))
    secondsFromNow = (datetime.timedelta(0, 60) + datetime.datetime.now()).strftime("%H%M")
    print(secondsFromNow)
    day = datetime.datetime.today().weekday()
    # guildDb.insertEntry("LECO6\nBSTAT\nELEARNING\n\nFT\nOHMOIY", day, secondsFromNow)
    # 0224
    # guildDb.deleteSingleEntry("LECO6\nBSTAT\nELEARNING\n\nFT\nOHMOIY", day, "0101")
