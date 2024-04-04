import pandas as pd
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont
from create_leagues import distribute_teams
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

leagues = {"Energi FK": "A",
           "NTNUI Samba": "A",
           "Marin FK": "B",
           "Omega FK": "C",
           "HSK": "C",
           "Janus FK": "B",
           "Tihlde Pythons": "B",
           "NTNUI Champs": "C",
           "FK Steindølene 1": "A",
           "Pareto FK": "A",
           "Wolves of Ballstreet": "B",
           "Datakameratene FK": "A",
           "Realkameratene FK": "D",
           "Smøreguttene FK": "D",
           "Hattfjelldal United": "B",
           "Chemie FK": "E",
           "Salt IF": "B",
           "Petroleum FK": "D",
           "Tim&Shænko": "D",
           "CAF": "D",
           "Omega Løkka": "D",
           "FK Steindølene 2": "A",
           "FK Hånd Til Munn": "C",
           "Knekken":"E",
           "MiT Fotball":"E",
           "Hybrida FK": "C",
           "Erudio Herrer": "C"}

season = "V24"

# Henter kamprapporter fra spreadsheet på nett
def readFromWeb():
    sheet_id = "2PACX-1vQuJYr5tl-zKfRpFUSsQaQ9yfxRa0U_k11gI9ke5PmFkBbdRROC5bLb8hks8r69KObhq4ISKapphr-9"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/e/{sheet_id}/pub?output=csv")

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
    with open(f'/Users/eliasheimdal/Desktop/tables/Scripts/Kamper/{season}/{avd.upper()}-sluttspill.xlsx', "rb") as file:
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
    writer = pd.ExcelWriter(f'/Users/eliasheimdal/Desktop/tables/Scripts/Kamper/{season}/{avd.upper()}-sluttspill.xlsx') 
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