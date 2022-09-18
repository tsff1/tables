import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from sklearn.utils import shuffle

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
    img = Image.open('TopScorerBG.png')
    size = img.size[1]
    draw = ImageDraw.Draw(img)
    fontS = ImageFont.truetype("Aller_Bd.ttf", 25)
    fontB = ImageFont.truetype("Aller_Bd.ttf", 30)
    y = 230
    x = 270
    xOff = [54, 64, 73]
    yOff = [146, 378, 591]
    scale = [200, 181, 163]

    i = 0
    for index, row in data.iterrows():
        if i < 3:
            draw.text((x, y),row[0],(0,0,0),font=fontB)
            draw.text((x + 300, y),row[1],(0,0,0),font=fontB)
            draw.text((x + 640, y),str(row[2]),(0,0,0),font=fontB)
            y = y + 222 - i*10
            logo = Image.open("Logoer - Runde/" + row[1] + ".png")
            size = (scale[i], scale[i])
            logo = logo.resize(size, Image.ANTIALIAS)
            img.paste(logo,(xOff[i], yOff[i]), mask = logo)
        else:
            x = 60
            y = 817 + 64*(i-3)
            draw.text((x, y),row[0],(0,0,0),font=fontS)
            draw.text((x + 510, y),row[1],(0,0,0),font=fontS)
            draw.text((x + 850, y),str(row[2]),(0,0,0),font=fontS)
        i+=1

    avdChr = chr(65 + avd)
    img.save('Avd_' + avdChr + '_TS.png')

def main(avd):
    data = readFromWeb(avd)
    data = shuffle(data)
    data = data.sort_values("Mål", ascending=False)
    createTopScore(data, avd)


# Velg avdeling: A = 0, B = 1
avd = 0

main(avd)