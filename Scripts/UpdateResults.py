import pandas as pd
import dataframe_image as dfi


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
            result = results.get(str(row[1])+"-"+str(row[5]))
            if result != None:
                matches.at[index, "H"] = int(result[0])
                matches.at[index, "B"] = int(result[-1])

    # Justerer kolonne-bredder
    writer = pd.ExcelWriter(f'C:/Users/Simen/tables2/tables/Scripts/Kamper/V23/{avd.upper()}-sluttspill.xlsx') 
    matches.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='')

    for column in matches:
        column_length = max(matches[column].astype(str).map(len).max(), len(column))
        col_idx = matches.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length+2)
    writer.close()

    
def main(avd):
    data_raw = readFromWeb()
    results = getResults(data_raw)             # Hentes fra google spreadsheet
    matches = getMatches(avd)                  # Hentes fra lokal excel
    insertResults(matches, results, avd)