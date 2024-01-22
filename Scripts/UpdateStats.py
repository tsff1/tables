from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from UpdateResults import readFromWeb
import string

leagues = {"Energi FK": "B",
           "NTNUI Samba": "A",
           "Marin FK": "B",
           "Omega FK": "A",
           "HSK": "A",
           "Janus FK": "B",
           "Tihlde Pythons": "A",
           "NTNUI Champs": "B",
           "FK Steindølene 1": "A",
           "Pareto FK": "B",
           "Wolves of Ballstreet": "A",
           "Datakameratene FK": "A",
           "Realkameratene FK": "B",
           "Smøreguttene FK": "B",
           "Hattfjelldal United": "B",
           "Chemie FK": "B",
           "Salt IF": "A",
           "Petroleum FK": "A",
           "Tim&Shænko": "B",
           "CAF": "A",
           "Omega Løkka": "B",
           "FK Steindølene 2": "B",
           "FK Hånd Til Munn": "B",
           "Knekken":"A",
           "MiT Fotball":"A",
           "Hybrida FK": "A",
           "Erudio Herrer": "A"}

season = "H23"

# Kode for spillerstatistikk
# Funkjsonen bruker dataen gitt fra df laget av kamprapport spreadsheet
# Den formaterer det i en dictionary 'stats'
# stats: {Spillernavn: [Lag, Mål, Gule kort, Røde kort], ...}
def getStats(data_raw: pd.DataFrame) -> dict:
    stats = {}
    for index, row in data_raw.iterrows():
        home = row[1]
        away = row[2]

        homePlayers = {}
        for elem in row[6].split("\n"):
            i = 1
            numFound = False
            elem = elem.strip()
            while True:
                try:
                    num = int(elem[:i])
                except ValueError:
                    if numFound:
                        homePlayers[num] = string.capwords(elem[(i-1):].strip())
                        break
                    else:
                        break
                else:
                    numFound = True
                    i += 1

        awayPlayers = {}
        for elem in row[11].split("\n"):
            i = 1
            numFound = False
            elem = elem.strip()
            while True:
                try:
                    num = int(elem[:i])
                except Exception:
                    if numFound:
                        awayPlayers[num] = string.capwords(elem[(i-1):].strip())
                        break
                    else:
                        break
                if i > len(elem):
                    break
                else:
                    numFound = True
                    i += 1

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
            except ValueError:
                print(f"Stats missing for game '{home} - {away}'. Problem: '{elem}'")


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
            except ValueError:
                print(f"Stats missing for game '{home} - {away}'. Problem: '{elem}'")


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
            except ValueError:
                print(f"Stats missing for game '{home} - {away}'. Problem: '{elem}'")

        # yellow cards away
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
            except ValueError:
                print(f"Stats missing for game '{home} - {away}'. Problem: '{elem}'")

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
            except ValueError:
                print(f"Stats missing for game '{home} - {away}'. Problem: '{elem}'")

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
            except ValueError:
                print(f"Stats missing for game '{home} - {away}'. Problem: '{elem}'")

    return stats

# Gjør om 'stats' dictionary til en df og sorterer etter gitt indeks
# index: 1 = yellow, 2 = red, 3 = goals
def createStats(index: int, stats: dict) -> pd.DataFrame:
    df = pd.DataFrame(stats)
    df = df.transpose()
    df = df.sample(frac=1)
    df = df.sort_values(by=index, ascending=False)
    return df

# Lager og lagrer et bilde av oversikt gitt indeks
# Obs: df må være sortert etter samme indeks som gitt
# index: 1 = yellow, 2 = red, 3 = goals
def createStatImage(df: pd.DataFrame, index: int):
    statname = [None, "Yellows", "Reds", "Goals"][index]
    img = Image.open(f'C:/Users/andre/Documents/NTNU/JS2023/TSFF/tables/Scripts/Backgrounds/Stat_bg.png')
    size = img.size[1]
    ydab = size/13
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("C:/Users/andre/Documents/NTNU/JS2023/TSFF/tables/Scripts/Fonts/Aller_Bd.ttf", 25)
    fontM = ImageFont.truetype("C:/Users/andre/Documents/NTNU/JS2023/TSFF/tables/Scripts/Fonts/Aller_Bd.ttf", 27)
    fontBig = ImageFont.truetype("C:/Users/andre/Documents/NTNU/JS2023/TSFF/tables/Scripts/Fonts/Aller_Bd.ttf", 30)

    i = 0
    for ind, row in df.iterrows():
        teamname = row[0]
        playername = ind
        stat = row[index]
        if stat == 0 or i >11:
            break

        y = (i+2)*ydab - 53
        logo = Image.open("C:/Users/andre/Documents/NTNU/JS2023/TSFF/tables/Scripts/Logoer - Runde/" + teamname + ".png")
        logo = logo.resize((50,50), Image.Resampling.LANCZOS)
        img.paste(logo,(400, int(y)-10), mask = logo)
        draw.text((52, y+2),playername,(0,0,0), font=font)
        draw.text((460, y),teamname,(0,0,0), font=font)
        draw.text((750, y),leagues[teamname],(0,0,0),font=font)
        draw.text((827, y-5),str(stat),(0,0,0),font=fontBig)
        i += 1

    img.save(f'C:/Users/andre/Documents/NTNU/JS2023/TSFF/tables/Scripts/Output/{season}/{statname}.png')

def main():
    print("\nUpdating stats:")
    print("Reading from web...")
    data_raw = readFromWeb()
    print("Collecting stats...")
    stats = getStats(data_raw)
    for i in range(1,4):
        if i == 1:
            print("Updating yellow cards...")
        elif i == 2:
            print("Updating red cards...")
        else:
            print("Updating goals...")
        df = createStats(i, stats)
        createStatImage(df, i)