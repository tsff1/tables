import pandas as pd
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont
from create_leagues import distribute_teams
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

leagues = {"Energi FK": "B",
           "NTNUI Samba": "B",
           "Marin FK": "B",
           "Omega FK": "B",
           "HSK": "C",
           "Janus FK": "A",
           "Tihlde Pythons": "C",
           "NTNUI Champs": "A",
           "FK Steindølene 1": "A",
           "Pareto FK": "C",
           "Wolves of Ballstreet": "A",
           "Datakameratene FK": "B",
           "Realkameratene FK": "C",
           "Smøreguttene FK": "A",
           "Chemie FK": "A",
           "SALT IF": "C",
           "Petroleum FK": "A",
           "Tim&Shænko": "A",
           "CAF": "B",
           "Omega Løkka": "C",
           "FK Steindølene 2": "A",
           "FK Hånd til Munn": "B",
           "Hybrida FK":"B",
           "MiT Fotball":"C",
           "Gladlaksen": "A",
           "Elektra FK":"B",
           "Erudio Herrer": "B",
           "FC BI United": "C",
           "Fornybar Stallions": "C",}

season = "H25"

# Henter kamprapporter fra spreadsheet på nett
def readFromWeb():
    sheet_id = "2PACX-1vQ86e6KlT5lYqGXgEF8AWNJIo7KMy-0WT1COZ4KsjuJ2hVi3N0ObXxd2Baq1q72O68cpdFoQb_ifWQE"  #"1EZOtOifu8_upktLS3_u9tI9oOWazQr6jLMinJnU-wG0"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/e/{sheet_id}/pub?output=csv")

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
    with open(f'/Users/evenlandmark/Desktop/tables/Scripts/Kamper/{season}/{avd.upper()}-Avdeling.xlsx', "rb") as file:
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
    writer = pd.ExcelWriter(f'/Users/evenlandmark/Desktop/tables/Scripts/Kamper/{season}/{avd.upper()}-Avdeling.xlsx') 
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