import json
import pandas as pd
import numpy as np
import os

filename = "data_sample/embeddings.jsonl"

with open(os.path.abspath(filename), "r", encoding="utf-8") as f:
    data = [
        json.loads(line)
        for line in open(os.path.abspath(filename), "r", encoding="utf-8")
    ]

def flattenizer(a):
    return (a[0],) + tuple(a[1])

dataframe_with_text_and_embeddings = pd.DataFrame()

processed_count = 0
mydata_expanded_flat = []
for line in data:
    if isinstance(line[1], list):
        continue
    else:
        info = flattenizer(
            [
                json.loads(json.dumps(line))[0]["input"],
                json.loads(json.dumps(line))[1]["data"][0]["embedding"],
            ]
        )
        mydata_expanded_flat.append(info)
        processed_count += 1

print(f"\nTotal embeddings converted to csv: {processed_count}\n")

def columns_index_maker():
    column_names = []
    column_names.append("wholetext")
    for _ in range(1536):
        column_names.append(str(_))

    return column_names


all_the_columns = columns_index_maker()

df = pd.DataFrame(mydata_expanded_flat, columns=all_the_columns)

def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))

def chonk_dataframe_and_make_csv_with_embeds(pddf, outputfile, chunks):
    """
    Recommended chonking from OpenAI, copypaste
    """
    for i, chunk in enumerate(chunker(pddf, chunks)):
        print("CHONKING TO CSV No: " + str(i))
        document_embeddings_i = pd.DataFrame(chunk)
        document_embeddings_i.to_csv(
            outputfile, mode="a", index=False, header=False if i > 0 else True
        )


if __name__ == "__main__":
    chonk_dataframe_and_make_csv_with_embeds(
        df, "data_sample/embeddings.csv", 1000
    )