import scrapy
from pathlib import Path
import zipfile


class WorldBankSpider(scrapy.Spider):
    name = "worldbank_spider"

    start_urls = [
        "https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv",  # Unemployment rate
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=csv",  # GDP growth rate
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv",  # GDP (current USD)
        "https://api.worldbank.org/v2/en/indicator/NE.IMP.GNFS.ZS?downloadformat=csv",  # Imports (% of GDP)
        "https://api.worldbank.org/v2/en/indicator/NE.EXP.GNFS.ZS?downloadformat=csv",  # Exports (% of GDP)
        "https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=csv",  # Inflation rate 
        "https://api.worldbank.org/v2/en/indicator/GC.REV.XGRT.GD.ZS?downloadformat=csv",  # Revenue (% of GDP)
        "https://api.worldbank.org/v2/en/indicator/SM.POP.REFG.OR?downloadformat=csv", # Refugiee Population
        "https://api.worldbank.org/v2/en/indicator/SM.POP.NETM?downloadformat=csv", # Net Migration,
        "https://api.worldbank.org/v2/en/indicator/TX.VAL.MRCH.CD.WT?downloadformat=csv", # Merchandise export
        "https://api.worldbank.org/v2/en/indicator/TM.VAL.MRCH.CD.WT?downloadformat=csv", # Merchandise import
        "https://api.worldbank.org/v2/en/indicator/TG.VAL.TOTL.GD.ZS?downloadformat=csv", # Merchandise Trade
    ]


    indicator_name_mapping = {
        "SL.UEM.TOTL.ZS": "Unemployment_rate",
        "NY.GDP.MKTP.KD.ZG": "GDP_growth_rate",
        "NY.GDP.MKTP.CD": "GDP_current_USD",
        "NE.IMP.GNFS.ZS": "Imports_percent_of_GDP",
        "NE.EXP.GNFS.ZS": "Exports_percent_of_GDP",
        "FP.CPI.TOTL.ZG": "Inflation_rate",
        "GC.REV.XGRT.GD.ZS": "Revenue_percent_of_GDP",
        "SM.POP.REFG.OR": "Refugiee_Population",
        "SM.POP.NETM": "Net_Migration",
        "TX.VAL.MRCH.CD.WT": "Merchandise_Export",
        "TM.VAL.MRCH.CD.WT": "Merchandise_Import",
        "TG.VAL.TOTL.GD.ZS": "Merchandise_Trade"
    }

    def save_and_extract_zip(self, response, file_name):
        """
        Save the ZIP file and extract its contents.
        """
        raw_dir = Path("data/raw/worldbank")
        raw_dir.mkdir(parents=True, exist_ok=True)

        zip_path = raw_dir / f"{file_name}.zip"
        with open(zip_path, "wb") as f:
            f.write(response.body)

        self.log(f"ZIP file saved at {zip_path}")

        extract_dir = raw_dir / file_name
        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            self.log(f"Extracted contents to {extract_dir}")
        except zipfile.BadZipFile:
            self.log(f"Failed to extract {zip_path}. Invalid ZIP file.")

    def parse(self, response):
        """
        Parse each response and call the function to save and extract data.
        """
        indicator_code = response.url.split("/")[-1].split("?")[0]
        file_name = self.indicator_name_mapping.get(indicator_code, indicator_code)
        self.save_and_extract_zip(response, file_name)
