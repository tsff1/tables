import pandas as pd
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont
from create_leagues import distribute_teams

leagues = {"Energi FK": "B",
           "NTNUI Samba": "A",
           "Marin FK": "B",
           "Omega FK": "B",
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
           "Omega Løkka": "A",
           "FK Steindølene 2": "B",
           "FK Hånd Til Munn": "B",
           "Knekken":"A",
           "MiT Fotball":"A",
           "Hybrida FK": "A",
           "Erudio Herrer": "A"}

season = "H23"

# Henter kamprapporter fra spreadsheet på nett
def readFromWeb():
    sheet_id = "2PACX-1vTfARjOGgNjbWeQnlO1E99wDIuv4gLde3MfHNqr5UF1yGGclOstZ4De2iriRT39usFvcZXnbat71Nbe"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/e/{sheet_id}/pub?output=csv")

# Henter ut resultater fra spreadsheet dataframe
# Returnerer dict på format {"Hjemmelag-Bortelag": "3-1", "Hjemmelag-Bortelag": "0-1", ...}
def getResults(data_raw):
    results = {}
    for index, row in data_raw.iterrows():
        print(row[1], row[2])
        key = row[1]+"-"+row[2]
        val = row[5]
        results[key] = val
    return results

# Henter kampopsett fra fil på github
def getMatches(avd):
    with open(f'C:/Users/Simen/tables2/tables/Scripts/Kamper/{season}/Avd {avd.upper()}.xlsx', "rb") as file:
        file = pd.read_excel(file)
    return file

# Oppdaterer excel-fil med resultater hentet fra kamprapporter
def insertResults(matches: pd.DataFrame, results, avd):

    for index, row in matches.iterrows():
        if str(row[0]) != "NaN":
            result = results.get(str(row[0])+"-"+str(row[4]))
            if result != None:
                result = result.split("-")
                matches.at[index, "H"] = int(result[0])
                matches.at[index, "B"] = int(result[-1])
                del results[str(row[0])+"-"+str(row[4])]

    # Justerer kolonne-bredder
    writer = pd.ExcelWriter(f'C:/Users/Simen/tables2/tables/Scripts/Kamper/{season}/Avd {avd.upper()}.xlsx') 
    matches.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='')

    for column in matches:
        column_length = max(matches[column].astype(str).map(len).max(), len(column))
        col_idx = matches.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length+2)
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