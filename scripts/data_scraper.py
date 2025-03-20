import scrapy
from pathlib import Path


class WorldBankSpider(scrapy.Spider):
    name = "worldbank_spider"

    # List of all URLs to download datasets
    start_urls = [
        "https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv",  # Unemployment rate
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=csv",  # GDP growth rate
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv",  # GDP (current USD)
        "https://api.worldbank.org/v2/en/indicator/NE.IMP.GNFS.ZS?downloadformat=csv",  # Imports (% of GDP)
        "https://api.worldbank.org/v2/en/indicator/NE.EXP.GNFS.ZS?downloadformat=csv",  # Exports (% of GDP)
        "https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=csv",  # Inflation rate
        "https://api.worldbank.org/v2/en/indicator/GC.REV.XGRT.GD.ZS?downloadformat=csv"  # Revenue (% of GDP)
    ]

    # Mapping of indicator codes to descriptive file names
    indicator_name_mapping = {
        "SL.UEM.TOTL.ZS": "Unemployment_rate",
        "NY.GDP.MKTP.KD.ZG": "GDP_growth_rate",
        "NY.GDP.MKTP.CD": "GDP_current_USD",
        "NE.IMP.GNFS.ZS": "Imports_percent_of_GDP",
        "NE.EXP.GNFS.ZS": "Exports_percent_of_GDP",
        "FP.CPI.TOTL.ZG": "Inflation_rate",
        "GC.REV.XGRT.GD.ZS": "Revenue_percent_of_GDP"
    }

    def download_data(self, response, file_name):
        """
        Generic function to download data and save it to the appropriate directory.
        """
        # Define the output directory (relative to your project structure)
        output_dir = Path("data/raw/worldbank")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save the dataset as a CSV file using the descriptive file name
        file_path = output_dir / f"{file_name}.csv"
        with open(file_path, "wb") as f:
            f.write(response.body)

        self.log(f"✅ File saved successfully at {file_path}")

    def parse(self, response):
        """
        Parse each response and call the generic function to save data.
        """
        # Extract indicator code from URL
        indicator_code = response.url.split("/")[-1].split("?")[0]

        # Get the descriptive file name from the mapping
        file_name = self.indicator_name_mapping.get(indicator_code, indicator_code)

        # Call the generic function to handle saving the data
        self.download_data(response, file_name)
