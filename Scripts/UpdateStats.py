from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from UpdateResults import readFromWeb
import string

leagues = {"Energi FK": "A",
           "NTNUI Samba": "A",
           "Marin FK": "A",
           "Omega FK": "A",
           "HSK": "A",
           "Janus FK": "A",
           "Tihlde Pythons": "B",
           "NTNUI Champs": "B",
           "FK Steindølene 1": "B",
           "Pareto FK": "B",
           "Wolves of Ballstreet": "B",
           "Datakameratene FK": "B",
           "Realkameratene FK": "C",
           "Smøreguttene": "C",
           "Hattfjelldal United": "C",
           "Chemie FK": "C",
           "DMFC": "C",
           "Salt IF": "C",
           "Petroleum FK": "D",
           "Balldura": "D",
           "Tim og Shænko": "D",
           "CAF": "D",
           "Omega Løkka": "D",
           "FK Steindølene 2": "D"}

season = "V23"

# Kode for spillerstatistikk
# Funkjsonen bruker dataen gitt fra df laget av kamprapport spreadsheet
# Den formaterer det i en dictionary 'stats'
# stats: {Spillernavn: [Lag, Mål, Gule kort, Røde kort], ...}
def getStats(data_raw: pd.DataFrame) -> dict:
    stats = {}
    for index, row in data_raw.iterrows():
        name = ""
        home = row[1]
        homePlayers = {}
        for elem in row[6].split():
            try:
                newNum = int(elem)
                homePlayers[oldNum] = string.capwords(name.strip())
                name = ""
                oldNum = newNum
            except ValueError:
                name += " " + elem
            except NameError:
                oldNum = newNum
        try:
            homePlayers[oldNum] = string.capwords(name.strip())
            homeStats = True
        except Exception:
            print(f"{home}'s stats missing for game {home}-{away}")
            homeStats = False

        if homeStats:
            del oldNum

        name = ""
        away = row[2]
        awayPlayers = {}
        for elem in row[11].split():
            try:
                newNum = int(elem)
                awayPlayers[oldNum] = string.capwords(name.strip())
                name = ""
                oldNum = newNum
            except ValueError:
                name += " " + elem
            except NameError:
                oldNum = newNum
        try:
            awayPlayers[oldNum] = string.capwords(name.strip())
            awayStats = True
        except Exception:
            print(f"{away}'s stats missing for game {home}-{away}")
            awayStats = False

        if awayStats:
            del oldNum

        try:
            yellowH = row[7].replace(" ", "").split()
        except Exception:
            yellowH = []
        try:
            redH = row[8].replace(" ", "").split()
        except Exception:
            redH = []
        try:
            goalsH = row[9].replace(" ", "").split()
        except Exception:
            goalsH = []

        try:
            yellowA = row[12].replace(" ", "").split()
        except Exception:
            yellowA = []
        try:
            redA = row[13].replace(" ", "").split()
        except Exception:
            redA = []
        try:
            goalsA = row[14].replace(" ", "").split()
        except Exception:
            goalsA = []


        # yellow cards home
        if homeStats:
            for elem in yellowH:
                elem = elem.split(":")
                try:
                    player = homePlayers[int(elem[0])]
                    try:
                        stats[player][1] += int(elem[-1])
                    except KeyError:
                        stats[player] = [home, int(elem[-1]), 0, 0]
                except KeyError:
                    print(f"Player number '{elem[0]}' not found in {home}'s team")


            # red cards home
            for elem in redH:
                elem = elem.split(":")
                try:
                    player = homePlayers[int(elem[0])]
                    try:
                        stats[player][2] += int(elem[-1])
                    except KeyError:
                        stats[player] = [home, 0, int(elem[-1]), 0]
                except KeyError:
                    print(f"Player number '{elem[0]}' not found in {home}'s team")


            # goals home
            for elem in goalsH:
                elem = elem.split(":")
                try:
                    player = homePlayers[int(elem[0])]
                    try:
                        stats[player][3] += int(elem[-1])
                    except KeyError:
                        stats[player] = [home, 0, 0, int(elem[-1])]
                except KeyError:
                    print(f"Player number '{elem[0]}' not found in {home}'s team")

        # yellow cards away
        if awayStats:
            for elem in yellowA:
                elem = elem.split(":")
                try:
                    player = awayPlayers[int(elem[0])]
                    try:
                        stats[player][1] += int(elem[-1])
                    except KeyError:
                        stats[player] = [away, int(elem[-1]), 0, 0]
                except KeyError:
                    print(f"Player number '{elem[0]}' not found in {away}'s team")

            # red cards away
            for elem in redA:
                elem = elem.split(":")
                try:
                    player = awayPlayers[int(elem[0])]
                    try:
                        stats[player][2] += int(elem[-1])
                    except KeyError:
                        stats[player] = [away, 0, int(elem[-1]), 0]
                except KeyError:
                    print(f"Player number '{elem[0]}' not found in {away}'s team")

            # goals away
            for elem in goalsA:
                elem = elem.split(":")
                try:
                    player = awayPlayers[int(elem[0])]
                    try:
                        stats[player][3] += int(elem[-1])
                    except KeyError:
                        stats[player] = [away, 0, 0, int(elem[-1])]
                except KeyError:
                    print(f"Player number '{elem[0]}' not found in {away}'s team")

    return stats

# Gjør om 'stats' dictionary til en df og sorterer etter gitt indeks
# index: 1 = yellow, 2 = red, 3 = goals
def createStats(index: int, stats: dict) -> pd.DataFrame:
    df = pd.DataFrame(stats)
    df = df.transpose()
    df = df.sort_values(by=index, ascending=False)
    return df

# Lager og lagrer et bilde av oversikt gitt indeks
# Obs: df må være sortert etter samme indeks som gitt
# index: 1 = yellow, 2 = red, 3 = goals
def createStatImage(df: pd.DataFrame, index: int):
    statname = [None, "Yellows", "Reds", "Goals"][index]
    img = Image.open(f'C:/Users/Simen/tables2/tables/Scripts/Backgrounds/Stat_bg.png')
    size = img.size[1]
    ydab = size/13
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("C:/Users/Simen/tables2/tables/Scripts/Fonts/Aller_Bd.ttf", 25)
    fontM = ImageFont.truetype("C:/Users/Simen/tables2/tables/Scripts/Fonts/Aller_Bd.ttf", 27)
    fontBig = ImageFont.truetype("C:/Users/Simen/tables2/tables/Scripts/Fonts/Aller_Bd.ttf", 30)

    i = 0
    for ind, row in df.iterrows():
        teamname = row[0]
        playername = ind
        stat = row[index]
        if stat == 0 or i >11:
            break

        y = (i+2)*ydab - 53
        logo = Image.open("C:/Users/Simen/tables2/tables/Scripts/Logoer - Runde/" + teamname + ".png")
        logo = logo.resize((50,50), Image.ANTIALIAS)
        img.paste(logo,(400, int(y)-10), mask = logo)
        draw.text((52, y+2),playername,(0,0,0), font=font)
        draw.text((460, y),teamname,(0,0,0), font=font)
        draw.text((750, y),leagues[teamname],(0,0,0),font=font)
        draw.text((827, y-5),str(stat),(0,0,0),font=fontBig)
        i += 1

    img.save(f'C:/Users/Simen/tables2/tables/Scripts/Output/{season}/{statname}.png')

def main():
    data_raw = readFromWeb()
    stats = getStats(data_raw)
    for i in range(1,4):
        df = createStats(i, stats)
        createStatImage(df, i)