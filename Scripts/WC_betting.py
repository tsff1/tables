import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from push import git_push

name_nation = {"Ruben": "Irland", "Iver": "Qatar", "Martin": "Nigeria",
               "Odin": "Tyskland", "Vegard": "Romania", "Simen": "Japan"}

def get_results():
    url = "https://fixturedownload.com/results/fifa-world-cup-2022"
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find_all("table")[0]

    df = pd.DataFrame(columns=['group', 'home', 'away', 'homeG', 'awayG'])

    j = 0
    for row in table.findAll('tr'):    
        # Find all data for each column
        columns = row.find_all('td')

        if(columns != []):
            start = columns[0].text.strip()[:2]
            if start in "123":
                home = columns[3].text.strip()
                away = columns[4].text.strip()
                group = columns[5].text.strip()[-1]
                score = columns[6].text.strip()
                homeG = score[0]
                awayG = score[-1]
                tmp = pd.DataFrame([[group, home, away, homeG, awayG]],
                                    columns=['group', 'home', 'away', 'homeG', 'awayG'])

                if homeG == "-":
                    break
                df = pd.concat([df, tmp])
                j += 1

    return df.reset_index()

def get_bets(results):
    file = open("C:/Users/Simen/tables2/tables/Scripts/Backgrounds/VM_22.csv")

    score = {}
    names = []

    i = 0
    n = -1
    for row in file:
        row = list(row.strip().split(";"))
        if row[0] != "" and row[1] == "":
            score[row[0]] = []
            names.append(row[0])
            n += 1
            i = -2
        # Its a game-row
        if i >= 0 and i <= 5:

            # Go through all cols
            for j in range(0, 16, 2):
                game_score = 0

                home, away = tuple(row[j].strip().split("-"))
                homeG, awayG = tuple(row[j+1].split("-"))
                homeG, awayG = int(homeG), int(awayG)

                # Find real result and compare
                for index, game in results.iterrows():
                    if game["home"] == home and game["away"] == away:
                        homeR = int(game["homeG"])
                        awayR = int(game["awayG"])
                        if homeR == homeG and awayR == awayG:
                            game_score = 2
                        else:
                            if homeR > awayR and homeG > awayG:
                                game_score = 1
                            elif homeR == awayR and homeG == awayG:
                                game_score = 1
                            elif homeR < awayR and homeG < awayG:
                                game_score = 1
                        score[names[n]].append(game_score)
                        break
        i += 1
    file.close()
    """"
    for player in score:
        print(player, score[player])
        print("-----------------------------\n\n")
    """
    for player in score:
        tot = sum(score[player])
        score[player] = tot

    sortedScore = []
    n = len(score)
    print(score)
    for i in range(n):
        top = float("-inf")
        topp = ""
        for player in score:
            if score[player] > top:
                top = score[player]
                topp = player
        sortedScore.append((topp, name_nation[topp], top))
        del score[topp]
        
    return sortedScore

def createTopScore(data):

    img = Image.open('C:/Users/Simen/tables2/tables/Scripts/Backgrounds/WC_test.png')
    size = img.size[1]
    draw = ImageDraw.Draw(img)
    fontS = ImageFont.truetype("C:/Users/Simen/tables2/tables/Scripts/Fonts/Aller_Bd.ttf", 85)
    fontB = ImageFont.truetype("C:/Users/Simen/tables2/tables/Scripts/Fonts/Aller_Bd.ttf", 100)
    y = 830
    x = 700
    xOff = [220, 248, 280]
    yOff = [505, 1298, 2030]
    scale = [680, 625, 560]

    prevGoals = 0
    prevNum = 1
    for index, row in enumerate(data):
        name = row[0]
        if row[2] == prevGoals:
            num = prevNum
        else:
            num = index + 1
        prevNum = num
        prevGoals = row[2]

        if index < 3:
            draw.text((x + 255, y),row[0],(0,0,0),font=fontB)
            draw.text((x + 1300, y),row[1],(0,0,0),font=fontB)
            draw.text((x + 2500, y),str(row[2]),(0,0,0),font=fontB)
            y = y + 750
            if index == 1:
                y-=50
            logo = Image.open(f"C:/Users/Simen/tables2/tables/Scripts/Bilder/{name}.png")
            size = (scale[index], scale[index])
            logo = logo.resize(size, Image.ANTIALIAS)
            img.paste(logo,(xOff[index], yOff[index]), mask = logo)
        else:
            x = 300
            y = 2820 + 220*(index-3)
            draw.text((x + 45, y),row[0],(0,0,0),font=fontS)
            draw.text((x + 1700, y),row[1],(0,0,0),font=fontS)
            draw.text((x + 2900, y),str(row[2]),(0,0,0),font=fontS)

    img.save('C:/Users/Simen/tables2/tables/Scripts/Bilder/WC_table.png')


results = get_results()
print(results)
sorted = get_bets(results)
createTopScore(sorted)
git_push()