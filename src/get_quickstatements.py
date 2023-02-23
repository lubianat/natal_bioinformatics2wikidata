import pandas as pd
from wdcuration import render_qs_url
from pathlib import Path

HERE = Path(__file__).parent.resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


def main():
    print(
        render_qs_url(
            add_speakers_to_event(
                curated_sheet_path=RESULTS.joinpath("curation_sheet.tsv"),
                event_id="Q116259311",
                reference_url="https://bioinfo.imd.ufrn.br/nbf/speakers",
            )
        )
    )


def add_speakers_to_event(curated_sheet_path, event_id, reference_url):
    df = pd.read_csv(curated_sheet_path, dtype={"id": object})
    qs = ""
    for i, row in df.iterrows():
        if row["wikidata_id"] != "NONE":
            speaker_id = row["wikidata_id"]
            property = "P823"
            wikidata_id = row["wikidata_id"]
            speaker_name = row["name"]
            qs += f'{event_id}|{property}|{wikidata_id}|S854|"{reference_url}"' + "\n"
            qs += f'{wikidata_id}|Aen|"{speaker_name}"' + "\n"
    return qs


if __name__ == "__main__":
    main()
