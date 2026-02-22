import pandas as pd

class AnimeDataLoader:
    def __init__(self, original_csv:str, processed_csv:str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv
        
    def load_and_process(self):
        df = pd.read_csv(self.original_csv, encoding='utf-8', on_bad_lines='skip').dropna()
        # sometimes csv can be some other encoding like latin, as utf-8 is standard, we will try to read with utf-8 and if it fails, we will try with latin encoding
        
        required_columns = {'Name', 'Genres', 'sypnopsis'}
        
        # here we are checking if the required columns are present in the csv file, if not we will raise an exception
        
        missing = required_columns - set(df.columns)
        
        if missing:
            raise ValueError(f"Missing columns {missing} in CSV file")
        
        df['combined_info'] = (
            "Title: " + df["Name"] + "..Overview: " + df['sypnopsis'] + "Genres : "+ df["Genres"]
        )
        
        df[['combined_info']].to_csv(self.processed_csv, index=False, encoding ="utf-8")
        
        return self.processed_csv