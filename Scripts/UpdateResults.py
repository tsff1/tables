import pandas as pd
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont
from create_leagues import distribute_teams
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

leagues = {"Energi FK": "B",
           "NTNUI Samba": "A",
           "Marin FK": "A",
           "Omega FK": "C",
           "HSK": "C",
           "Janus FK": "B",
           "Tihlde Pythons": "B",
           "NTNUI Champs": "C",
           "FK Steindølene 1": "A",
           "Pareto FK": "B",
           "Wolves of Ballstreet": "A",
           "Datakameratene FK": "A",
           "Realkameratene FK": "C",
           "Smøreguttene FK": "D",
           "Hattfjelldal United": "B",
           "Chemie FK": "E",
           "SALT IF": "A",
           "Petroleum FK": "E",
           "Tim&Shænko": "D",
           "CAF": "E",
           "Omega Løkka": "E",
           "FK Steindølene 2": "B",
           "FK Hånd til Munn": "C",
           "Knekken":"D",
           "MiT Fotball":"E",
           "CKK": "D",
           "Elektra FK":"E",
           "Erudio Herrer": "D",
           "FC BI United":"D",
           "Sparkekameratene": "C",
           "Dronning Maud FC": "E",}

season = "V25"

# Henter kamprapporter fra spreadsheet på nett
def readFromWeb():
    sheet_id = "1_uadIIN5-d0bXuVIzYO6vbe-QwbJOvgG2nwMbkJW8UY"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/pub?output=csv")

# Henter ut resultater fra spreadsheet dataframe
# Returnerer dict på format {"Hjemmelag-Bortelag": "3-1", "Hjemmelag-Bortelag": "0-1", ...}
def getResults(data_raw):
    results = {}
    for index, row in data_raw.iterrows():
        # Convert row[1] and row[2] to strings and handle NaN values
        key = str(row[1]) if pd.notna(row[1]) else ""
        key += "-" + (str(row[2]) if pd.notna(row[2]) else "")
        
        # Ensure val is also handled correctly
        val = row[5] if pd.notna(row[5]) else None
        
        # Store the result
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