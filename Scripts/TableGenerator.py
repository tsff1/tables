from turtle import home

import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import date
import UpdateResults as ur

season = "V25"

# Henter data fra spreadsheet. 
# return: pandas dataframe med data
def readFromWeb(avd):
    avd = avd.lower()
    if avd == "a":
        sheet_id = "1h-EGu8ROHBv04nqdhhvT3wQmFzWIvpPG4aUujfGwdmI" # Sluttspill A
    elif avd == "b":
        sheet_id = "1P9xLBwLwYf7jh-BulnsDAf1LmURftxupsi7fX_I8OE4" # Sluttspill B
    elif avd == "c":
        sheet_id = "1nyB8S0EId5ZYwuWht3a88WKrHYaH-rN7vJy2M3ChuNk" # Sluttspill C
    elif avd == "d":
        sheet_id = "1bHR14x_Q20B-WPMojQ3tqj6frJYuxJQz5_oQ0F_9SBs" # Sluttspill D
    elif avd == "e":
        sheet_id = "1M5VCjrirY4kH-3yQ2Bj2RXQpfBR-5VbNKBzmbQeK0eE" # Sluttspill E

    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv", verify=False)

# Leser gjennom dataframe og henter ut interessant data
# dataframe: pandas dataframe med data
# return: 2D-liste med kamper og resultater

def locateData(dataframe):
    dataList = []
    for index, row in dataframe.iterrows():
        if str(row.iloc[0])[:4] not in ["Week", "nan"]:
            newRow = [row[i] for i in [0,1,3,4]]
            dataList.append(newRow)
    return dataList

# Leser gjennom dataList og regner ut lags resultater til en dictionary
# Value-format: lagindeks, kamper spilt, vunnet, uavgjort, tapt, mål for, mål mot, målforskjell, poeng
# Return: matrise med et lag på hver rad, liste med lagnavn
def getData(dataList, nteams):
    print(dataList)
    teamData = {}
    teamNames = []
    for i, row in enumerate(dataList):
        row[0] = row[0].strip()
        row[-1] = row[-1].strip()
        if str(row[1]) != "nan" and str(row[2]) != "nan":
            row[2], row[1] = int(row[2]), int(row[1])
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
        
        if row[0] not in teamData:
            teamNames.append(row[0])
            teamData[row[0]] = [len(teamNames)-1,0,0,0,0,0,0,0,0]

        if row[-1] not in teamData:
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
def createTable(sortedTeams, teamNames, avd, nteams):
    img = Image.open(f'/Users/evenlandmark/Desktop/tables/Scripts/Backgrounds/V25/Tabel_bg_{avd.upper()}_{season}.png')
    size = img.size[1]
    ydab = size/(nteams+1)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/Users/evenlandmark/Desktop/tables/Scripts/Fonts/Aller_Bd.ttf", 25)

    for i, row in enumerate(sortedTeams):
        name = teamNames[int(row[0])]
        y = (i+2)*ydab - 53
        logo = Image.open("/Users/evenlandmark/Desktop/tables/Scripts/Logoer - Runde/" + name + ".png")
        logo = logo.resize((50,50), Image.Resampling.LANCZOS)
        img.paste(logo,(55, int(y)-10), mask = logo)
        draw.text((115, y),name,(0,0,0), font=font)
        for j, col in enumerate(row[1:]):
            x = 407 + j * 60
            draw.text((x, y),str(int(col)),(0,0,0),font=font)

    img.save(f'/Users/evenlandmark/Desktop/tables/Scripts/Output/{season}/' + avd.upper() + '-table.png')

def updateTime(avd, stats = False):
    today = date.today()
    img = Image.open('/Users/evenlandmark/Desktop/tables/Scripts/Backgrounds/Time_bg.png')
    img = img.resize((400, 40), Image.Resampling.LANCZOS)
    fontT = ImageFont.truetype("/Users/evenlandmark/Desktop/tables/Scripts/Fonts/Aller_Bd.ttf", 30)
    draw = ImageDraw.Draw(img)
    draw.text((20, 0),"Sist oppdatert: " + today.strftime("%d/%m/%Y"),(0,0,0),font=fontT)
    if stats:
        img.save(f'/Users/evenlandmark/Desktop/tables/Scripts/Output/{season}/Stats_Update.png')
    else:
        img.save(f'/Users/evenlandmark/Desktop/tables/Scripts/Output/{season}/'+ avd.upper()+ '-Update.png')

def main(avd, nteams):
    ur.main(avd)
    updateTime(avd, stats=True)
    #df = readFromWeb(avd)

    df = ur.getMatches(avd)
    dataList = locateData(df)
    teamResults, teamNames = getData(dataList,nteams)
    sortedTeamResults = sortTeams(teamResults, teamNames)
    #printTable(sortedTeamResults, teamNames)
    createTable(sortedTeamResults,teamNames,avd,nteams)
    updateTime(avd)

if __name__ == "__main__":
    main()