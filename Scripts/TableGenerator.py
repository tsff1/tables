from turtle import home

import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Henter data fra spreadsheet. 
# avd: 0 = A, 1 = B
# return: pandas dataframe med data
def readFromWeb(avd):
    if avd:
        sheet_id = "1LgMuGeBLz6pPJ7UzxWTTYRUK6uWNe3n34JeG0djM36U" # Avdeling B
    else:
        sheet_id = "1ltRMXLKCC3XdhglsLxQT6W4u2lX7RcuwgttWd5ek6lA" # Avdeling A
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Leser gjennom dataframe og henter ut interessant data
# dataframe: pandas dataframe med data
# return: 2D-liste med kamper og resultater

def locateData(dataframe):
    dataList = []
    for index, row in dataframe.iterrows():
        if str(row[0])[:4] not in ["Week", "nan"]:
            newRow = [row[i] for i in [0,1,3,4]]
            dataList.append(newRow)
    return dataList

# Leser gjennom dataList og regner ut lags resultater til en dictionary
# Value-format: lagindeks, kamper spilt, vunnet, uavgjort, tapt, mål for, mål mot, målforskjell, poeng
# Return: matrise med et lag på hver rad, liste med lagnavn
def getData(dataList):
    teamData = {}
    teamNames = []
    for i, row in enumerate(dataList):
        if str(row[1]) != "nan" and str(row[2]) != "nan":
            if row[2] > row[1]:
                awayPoints = 3
                homePoints = 0
            elif row[2] == row[1]:
                homePoints = 1
                awayPoints = 1
            else:
                awayPoints = 0
                homePoints = 3
            
            if row[0] in teamData:
                teamData[row[0]][1] += 1
                teamData[row[0]][2] += homePoints//3
                teamData[row[0]][3] += homePoints%3
                teamData[row[0]][4] += int(not bool(homePoints))
                teamData[row[0]][5] += row[1]
                teamData[row[0]][6] += row[2]
                teamData[row[0]][7] += row[1] - row[2]
                teamData[row[0]][8] += homePoints
                
            else:
                teamNames.append(row[0])
                teamData[row[0]] = [len(teamNames)-1,1,homePoints//3,homePoints%3,int(not bool(homePoints)),row[1],row[2],row[1]-row[2],homePoints]

            if row[-1] in teamData:
                teamData[row[-1]][1] += 1
                teamData[row[-1]][2] += awayPoints//3
                teamData[row[-1]][3] += awayPoints%3
                teamData[row[-1]][4] += int(not bool(awayPoints))
                teamData[row[-1]][5] += row[2]
                teamData[row[-1]][6] += row[1]
                teamData[row[-1]][7] += row[2] - row[1]
                teamData[row[-1]][8] += awayPoints
            else:
                teamNames.append(row[-1])
                teamData[row[-1]] = [len(teamNames)-1,1,awayPoints//3,homePoints%3,int(not bool(awayPoints)),row[2],row[1],row[2]-row[1],awayPoints]
        elif i < 6:
            teamNames.append(row[0])
            teamData[row[0]] = [len(teamNames)-1,0,0,0,0,0,0,0,0]

            teamNames.append(row[-1])
            teamData[row[-1]] = [len(teamNames)-1,0,0,0,0,0,0,0,0]
    
    return teamData, teamNames

# Sorterer teamResults ut fra poeng, målforskjell, mål scoret
# Return: matrise med lag sortert (se getData() for detaljer)
def sortTeams(teamResults, teamNames):
    data = np.zeros(9*len(teamNames))
    data = data.reshape((len(teamNames),9))
    i = 0
    for key, value in teamResults.items():
        data[i] = np.array(value)
        i += 1
    data = data[data[:,-4].argsort()]                   # sort by GS
    data = data[data[:, -2].argsort(kind='mergesort')]  # sort by GD
    data = data[data[:, -1].argsort(kind='mergesort')]  # sort by points
    data = np.flip(data,0)
    return data

# Printer tabell til konsoll, ment for debugging
def printTable(sortedTeams, teamNames):
    print("Team", 15*" ","G", "  W", "  D", "  L", "  GS", " GA", " GD", " P")
    print("----------------------------------------------------")
    for row in sortedTeams:
        name = teamNames[int(row[0])]
        print(name, (20 - len(name))*" ", end = "")
        for element in row[1:]:
            print(int(element), end=((4-len(str(int(element))))*" "))
        print()

# Lager bilde av tabell
# sortedTeams: numpy-matrise med sorterte lagresultater
# teamNames: liste med lagnavn, avd: 0 = A, 1 = B
# Lagres til Avd_X_table.png
def createTable(sortedTeams, teamNames, avd):
    img = Image.open('Tabel_bg.png')
    size = img.size[1]
    ydab = size/13
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Aller_Bd.ttf", 25)

    for i, row in enumerate(sortedTeams):
        name = teamNames[int(row[0])]
        y = (i+2)*ydab - 53
        draw.text((60, y),name,(0,0,0),font=font)
        for j, col in enumerate(row[1:]):
            x = 407 + j * 60
            draw.text((x, y),str(int(col)),(0,0,0),font=font)

    avdChr = chr(65 + avd)
    img.save('Avd_' + avdChr + '_table.png')

def main(avd):
    df = readFromWeb(avd)
    dataList = locateData(df)
    teamResults, teamNames = getData(dataList)
    sortedTeamResults = sortTeams(teamResults, teamNames)
    createTable(sortedTeamResults,teamNames,avd)



# Velg avdeling: A = 0, B = 1
avd = 0

main(avd)