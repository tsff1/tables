import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from sklearn.utils import shuffle
import os.path
from datetime import date

def readFromWeb(avd):
    if avd:
        sheet_id = "1IcfefQd7Vfdl9oxBo7I-5s_RRUrD9KWuSyBRyHUJeV8" # Avdeling B
    else:
        sheet_id = "1QrbXxgceluPlQ6mJEbF6kTMHP_8JL0mzYHS-oDM09O0" # Avdeling A
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

def locateData(dataframe):
    dataList = []
    for index, row in dataframe.iterrows():
        if index > 0:
            newRow = [row[i] for i in [0,1,3,4]]
            dataList.append(newRow)
    return dataList

def createTopScore(data, avd):
    img = Image.open('Scripts/Backgrounds/TopScorerBG.png')
    size = img.size[1]
    print(size)
    draw = ImageDraw.Draw(img)
    fontS = ImageFont.truetype("Scripts/Fonts/Aller_Bd.ttf", 25)
    fontB = ImageFont.truetype("Scripts/Fonts/Aller_Bd.ttf", 30)
    y = 230
    x = 15
    xOff = [54, 64, 73]
    yOff = [146, 378, 591]
    scale = [200, 181, 163]

    prevGoals = 0
    prevNum = 1
    for index, row in data.iterrows():

        if row[2] == prevGoals:
            num = prevNum
        else:
            num = index + 1
        prevNum = num
        prevGoals = row[2]

        if index < 3:
            draw.text((x, y),str(num)+".",(0,0,0),font=fontB)
            draw.text((x + 255, y),row[0],(0,0,0),font=fontB)
            draw.text((x + 565, y),row[1],(0,0,0),font=fontB)
            draw.text((x + 895, y),str(row[2]),(0,0,0),font=fontB)
            y = y + 222 - index*10
            if os.path.exists("Scripts/Toppscorers/" + row[0] + ".png"):
                logo = Image.open("Scripts/Toppscorers/" + row[0] + ".png")
            else:
                logo = Image.open("Scripts/Logoer - Runde/" + row[1] + ".png")
            size = (scale[index], scale[index])
            logo = logo.resize(size, Image.ANTIALIAS)
            img.paste(logo,(xOff[index], yOff[index]), mask = logo)
        else:
            x = 15
            y = 817 + 64*(index-3)
            draw.text((x, y),str(num)+".",(0,0,0),font=fontS)
            draw.text((x + 45, y),row[0],(0,0,0),font=fontS)
            draw.text((x + 555, y),row[1],(0,0,0),font=fontS)
            draw.text((x + 895, y),str(row[2]),(0,0,0),font=fontS)

    avdChr = chr(65 + avd)
    img.save('Scripts/Output/Avd_' + avdChr + '_TS.png')

def updateTime(avd):
    avdChr = chr(65 + avd)
    today = date.today()
    img = Image.open('Scripts/Backgrounds/Time_bg.png')
    img = img.resize((400, 40), Image.ANTIALIAS)
    fontT = ImageFont.truetype("Scripts/Fonts/Aller_Bd.ttf", 30)
    draw = ImageDraw.Draw(img)
    draw.text((20, 0),"Sist oppdatert: " + today.strftime("%d/%m/%Y"),(0,0,0),font=fontT)
    img.save('Scripts/Output/Avd_' + avdChr + '_Update.png')


def main(avd):
    data = readFromWeb(avd)
    data = shuffle(data)
    data = data.sort_values("Mål", ascending=False)
    data = data.reset_index(drop=True)
    createTopScore(data, avd)
    updateTime(avd)


# Velg avdeling: A = 0, B = 1
avd = 0

main(avd)