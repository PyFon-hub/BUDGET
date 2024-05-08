import pandas as pd
from io import StringIO
import hashlib

class data_for_app():
    def __init__(self, input_file) -> None:
        with open(input_file, encoding='utf-8') as file:
            text = file.read()

            #Impoving data for further action
            text = text.replace("#Kwota;", "Kwota") 
            text = text.replace(";;", "") 
            text = text.replace("#", "")
            
            #Checing the data
            if(text[0:13] == "Data operacji"): 
                data = StringIO(text)
                df = pd.read_csv(data, sep= ";", decimal=',')
            else:
                data = StringIO(text)
                df = pd.read_csv(data, sep= ";", decimal=',', skiprows = 25)
            
        #Creating new unique ID and new column 'Waluta'
        df.insert(0, "Id", df.apply(lambda row: hashlib.sha256(str(row).encode('utf-8')).hexdigest()[:20], axis = 1))
        df.insert(df.shape[1], "Waluta", df.Kwota.apply(lambda row: row[-3:]))

        #Making more readable descriptions
        df["Opis operacji"] = df["Opis operacji"].apply(lambda row: ' '.join(row.split()))
        df.Kwota = df.Kwota.apply(lambda row: float(row[:-4].replace(" ", "").replace(",", ".")))

        try:
            main_data = pd.read_csv("../Data/BankData_for_app.csv")
        # Concatenate and remove duplicates
            main_data = pd.concat([main_data, df], ignore_index=True).drop_duplicates().reset_index(drop=True)
        except:
            main_data = df.reset_index(drop=True)
        # Save to csv file
            main_data.to_csv("../Data/BankData_for_app.csv", index=False)
        

