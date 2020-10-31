import pandas as pd
import numpy as np
import tabulate

# removes any unwanted unamed columns
df = pd.read_excel("1.xlsx", index_col=[0])
# removes all the \n & and \x0c thingy
df = df.replace(r"\\n", " ", regex=True)
df = df.replace(r"\\x0c", " ", regex=True)

# removes whatever that is not digits in the time column
df[0] = df[0].str.replace(r"\D", "", regex=True)
# words to remove
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

# creates new row on top of the xl sheet with headers
new_row = pd.DataFrame(
    {0: "TIME", 1: "MON", 2: "TUES", 3: "WED", 4: "THURS", 5: "FRI", 6: "SAT"},
    index=[1],
)
df = pd.concat([new_row, df]).reset_index(drop=True)

# this code looks like shit, but it works
# formats the timing
def formatTime():
    for x in range(1, len(df[0])):
        df[0][x] = df[0][x][:4] + "-" + df[0][x][4:]
    print("Format completed.")
    # print(df[0])


# random large number for it to iterrate
def replaceCommon():
    for x in range(100):
        try:
            for char in delWords:
                df[x] = df[x].str.replace(char, "")
        except KeyError:
            print("Replacing completed.")
            break
    # print(df[1])


def removeBeforeLessonTypes():
    for types in lessonTypes:
        for colNo in range(len(df.columns)):
            for rowNo in range(len(df)):
                try:

                    index = df[colNo][rowNo].index(types)
                    df[colNo][rowNo] = df[colNo][rowNo][index:]

                except:
                    pass
    print("Removed completed.")


formatTime()
replaceCommon()
removeBeforeLessonTypes()
df.to_csv("newShit.csv")
