import requests
import pandas as pd
from bs4 import BeautifulSoup
from wdcuration import run_multiple_searches
import asyncio
from pathlib import Path

HERE = Path(__file__).parent.resolve()
RESULTS = HERE.parent.joinpath("results").resolve()

url = "https://bioinfo.imd.ufrn.br/nbf/speakers"
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")
output_file_path = RESULTS.joinpath("curation_sheet.tsv")

# HTML locator identified with help of https://webscraper.io/
names = soup.find_all("h5")
clean_names = [name.text.split("–")[0].split("-")[0] for name in names]


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(
    run_multiple_searches(
        clean_names,
        excluded_types=[],
        fixed_type="Q5",
    )
)
results = loop.run_until_complete(future)

print(results)

df = pd.DataFrame({"name": clean_names})
df["wikidata_id"] = df["name"].map({k: v["id"] for k, v in results.items()})
df["wikidata_label"] = df["name"].map({k: v["label"] for k, v in results.items()})
df["wikidata_description"] = df["name"].map(
    {k: v["description"] for k, v in results.items()}
)

df.to_csv(output_file_path, index=False)
