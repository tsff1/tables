import pandas as pd
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont

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

# Henter kamprapporter fra spreadsheet på nett
def readFromWeb():
    sheet_id = "1kuCumwCYQw2ksqtRrtDhMhPtuN8XHLJmi_iacrYSeME"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Henter ut resultater fra spreadsheet dataframe
# Returnerer dict på format {"Hjemmelag-Bortelag": "3-1", "Hjemmelag-Bortelag": "0-1", ...}
def getResults(data_raw):
    results = {}
    for index, row in data_raw.iterrows():
        key = row[1]+"-"+row[2]
        val = row[5]
        results[key] = val
    return results

# Henter kampopsett fra fil på github
def getMatches(avd):
    with open(f'C:/Users/Simen/tables2/tables/Scripts/Kamper/V23/{avd.upper()}-sluttspill.xlsx', "rb") as file:
        file = pd.read_excel(file)
    return file

# Oppdaterer excel-fil med resultater hentet fra kamprapporter
def insertResults(matches: pd.DataFrame, results, avd):

    for index, row in matches.iterrows():
        if str(row[0]) != "NaN":
            result = results.get(str(row[0])+"-"+str(row[4]))
            if result != None:
                matches.at[index, "H"] = int(result[0])
                matches.at[index, "B"] = int(result[-1])
                del results[str(row[0])+"-"+str(row[4])]

    # Justerer kolonne-bredder
    writer = pd.ExcelWriter(f'C:/Users/Simen/tables2/tables/Scripts/Kamper/V23/{avd.upper()}-sluttspill.xlsx') 
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