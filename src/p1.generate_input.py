import pandas as pd
import json

filename = "data_sample/converted.jsonl"

# To make sure the title and url is included in vectorization as well
# it would be better to have these as separate database properties, so that will be changed
def combine_text_to_one_column(df):
    for row in df:
        row['model'] = "text-embedding-ada-002"
        row['input'] = "Title: " + row['title'] + " url: " + row["url"] + " content: " + row["content"]

        # Drop the rows that shouldn't be vectorized
        del row['title']
        del row['url']
        del row['content']
    
    with open(filename, "w") as f:
        for row in df:
            json_string = json.dumps(row)
            f.write(json_string + "\n")


if __name__ == "__main__":
    df = pd.read_json(
        path_or_buf="data_sample/raw_info.json",
        encoding="utf-8",
    )
    
    combine_text_to_one_column(df=df['informationBlobs'])
