import pandas as pd
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont
from create_leagues import distribute_teams
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

leagues = {"Energi FK": "B",
           "NTNUI Samba": "C",
           "Marin FK": "A",
           "Omega FK": "A",
           "HSK": "C",
           "Janus FK": "C",
           "Tihlde Pythons": "C",
           "NTNUI Champs": "B",
           "FK Steindølene 1": "A",
           "Pareto FK": "B",
           "Wolves of Ballstreet": "C",
           "Datakameratene FK": "B",
           "Realkameratene FK": "B",
           "Smøreguttene FK": "C",
           "Hattfjelldal United": "A",
           "Chemie FK": "A",
           "SALT IF": "B",
           "Petroleum FK": "C",
           "Tim&Shænko": "B",
           "CAF": "B",
           "Omega Løkka": "B",
           "FK Steindølene 2": "A",
           "FK Hånd Til Munn": "A",
           "Knekken":"A",
           "MiT Fotball":"C",
           "CKK": "C",
           "Elektra FK":"A",
           "Erudio Herrer": "A",
           "FC BI United":"B",
           "Sparkekameratene": "C",
           "Dronning Maud FC": "C",}

season = "H24"

# Henter kamprapporter fra spreadsheet på nett
def readFromWeb():
    sheet_id = "1_uadIIN5-d0bXuVIzYO6vbe-QwbJOvgG2nwMbkJW8UY"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/pub?output=csv")

# Henter ut resultater fra spreadsheet dataframe
# Returnerer dict på format {"Hjemmelag-Bortelag": "3-1", "Hjemmelag-Bortelag": "0-1", ...}
def getResults(data_raw):
    results = {}
    for index, row in data_raw.iterrows():
        #print(row[1], row[2])
        key = row[1]+"-"+row[2]
        val = row[5]
        results[key] = val
    return results

# Henter kampopsett fra fil på github
def getMatches(avd):
    with open(f'/Users/eliasheimdal/Desktop/tables/Scripts/Kamper/{season}/Avd-{avd.upper()}.xlsx', "rb") as file:
        file = pd.read_excel(file)
    return file

# Oppdaterer excel-fil med resultater hentet fra kamprapporter
def insertResults(matches: pd.DataFrame, results, avd):

    for index, row in matches.iterrows():
        if str(row.iloc[0]) != "NaN":
            result = results.get(str(row.iloc[0])+"-"+str(row.iloc[4]))
            if result != None:
                result = result.split("-")
                matches.at[index, "H"] = int(result[0])
                matches.at[index, "B"] = int(result[-1])
                del results[str(row[0])+"-"+str(row[4])]

    # Justerer kolonne-bredder
    writer = pd.ExcelWriter(f'/Users/eliasheimdal/Desktop/tables/Scripts/Kamper/{season}/Avd-{avd.upper()}.xlsx') 
    matches.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='')

    for column in matches:
        column_length = max(matches[column].astype(str).map(len).max(), len(column))
        col_idx = matches.columns.get_loc(column)
    writer.close()

    for teams, result in results.items():
        if result != None:
            teams = teams.split("-")
            if leagues[teams[0]] == avd.upper():
                print("Match '" + teams[0] + " - " + teams[1] + "' not found")

    
def main(avd):
    data_raw = readFromWeb()
    results = getResults(data_raw)             # Hentes fra google spreadsheet
    matches = getMatches(avd)                  # Hentes fra lokal excel
    insertResults(matches, results, avd)

if __name__ == "__main__":
    main()