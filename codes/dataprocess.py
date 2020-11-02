# includes cleaning the excel sheet from the convert and,
# outputing the timetable as a string for output in discord.

import pandas as pd
import numpy as np


def cleanExcel():
    # data precleaning ======================================
    # removes any unwanted unamed columns
    df = pd.read_excel("1.xlsx", index_col=[0])
    # removes all the \n & and \x0c thingies
    df = df.replace(r"\\n", " ", regex=True)
    df = df.replace(r"\\x0c", " ", regex=True)
    # removes whatever that is not digits in the time column
    df[0] = df[0].str.replace(r"\D", "", regex=True)
    # =======================================================
    new_row = pd.DataFrame(
        {0: "TIME", 1: "MON", 2: "TUES", 3: "WED", 4: "THURS", 5: "FRI", 6: "SAT"},
        index=[1],
    )
    days_to_number = {"MON": 0, "TUES": 1, "WED": 2, "THURS": 3, "FRI": 4, "SAT": 5}
    df = pd.concat([new_row, df]).reset_index(drop=True)
    # list is pretty limited, gonna need more keywords ://
    # words to remove =====================
    delWords = [
        "WEEK",
        "EEK",
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "1-17",
    ]
    lessonTypes = ["LEC", "LAB", "TUT"]
    # =====================================

    # creates new row on top of the xl sheet with headers

    # this code looks like shit, but it works
    # formats the timing
    def formatTime():
        for x in range(1, len(df[0])):
            df[0][x] = df[0][x][:4]
        print("Format completed.")
        # print(df[0])

    # random large number for it to iterrate
    # gonna add more keywords
    def replaceCommon():
        for x in range(100):
            try:
                for char in delWords:
                    df[x] = df[x].str.replace(char, "")
            except KeyError:
                print("Replacing completed.")
                break
        # print(df[1])

    def removeStrBeforeLessonTypes():
        for types in lessonTypes:
            for colNo in range(len(df.columns)):
                for rowNo in range(len(df)):
                    try:
                        # going thru each individual cell and replacing shit,
                        # probably easier way to do this but im too lazy.
                        index = df[colNo][rowNo].index(types)
                        df[colNo][rowNo] = df[colNo][rowNo][index:]

                    except:
                        pass
        print("Removed completed.")

    def collectEntry():
        entryForClass = []
        for colNo in range(1, len(df.columns)):
            for rowNo in range(1, len(df)):
                post = {"day": "", "time": "", "subject": ""}
                post["day"] = days_to_number[df[colNo][0]]
                post["time"] = df[0][rowNo]
                post["subject"] = df[colNo][rowNo].strip()
                if post["subject"] == "":
                    continue
                else:
                    entryForClass.append(post)
        print("Entries have been recorded.")
        return entryForClass

    # removes the Sat column if its empty
    # cant put this a function, itll break
    lastCol = df.columns[-1]
    x = df[lastCol][1:].sum()
    print(x)
    if x.strip() == "":
        df = df[df.columns[:-1]]

    # output to csv, please include path
    # added this into a giant function cos the code needs to be ran sequentially
    # df.to_excel(path of file)
    # df.to_excel("newshit.xlsx")
    formatTime()
    replaceCommon()
    removeStrBeforeLessonTypes()
    # print(tabulate(df))
    # print(collectEntry())
    return collectEntry()
