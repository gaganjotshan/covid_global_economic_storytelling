import pandas as pd
import os

COUNTRIES = ['Russian Federation', 'United States', 'China']

def load_and_transform(csv_file: str, start_year: int=2010, end_year: int=2023) -> pd.DataFrame:
    indicator_name = csv_file.split('/')[4]
    df = pd.read_csv(csv_file, skiprows=4)
    df = df[['Country Name', *map(str, range(start_year, end_year+1))]].rename(columns={'Country Name': 'country'})
    df = pd.melt(df, id_vars='country', var_name='year', value_name=indicator_name)
    df = df[df['country'].isin(COUNTRIES)]
    return df

def process(directory: str) -> None:
    df = None
    for dir in os.listdir(directory):
        if os.path.isdir(directory + '/' + dir):
            for file_name in os.listdir(directory + dir):
                if file_name[-4:] == '.csv' and 'Metadata' not in file_name:
                    if df is not None:
                        df = df.merge(load_and_transform(directory + '/' + dir + '/' + file_name), on=['country', 'year'])
                    else:
                        df = load_and_transform(directory + '/' + dir + '/' + file_name)
    df.to_csv('data/processed/global_dataset.csv')

if __name__ == "__main__":
    process("data/raw/worldbank/")