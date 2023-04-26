# Pinecone index filler
Note: This implementation was developed as a proof-of-concept of how to vectorize and publish data to pinecone. It is currently not in use anywhere and that is expected to remain true in the future.

This implementation is largely reliant on the file `p2.api_request_parallel_processor.py`, which is an example provided in the OpenAI Playbook.

#### p1
Generates the wholetext to vectorize, to make sure that the title is included in vectorization as well. Right now the source url is included but that is probably a bad idea, so it should change. Will have to understand the parallel processor better before I can figure out how to *not* vectorize it, but still include it in the metadata.

Converts the data to jsonl and appends a "job" to each datapoint, which is the required input for the `p3.api_request_parallel_processor.py`

#### p2
Example provided by OpenAI, performs the assigned job (vectorization) on each article

To run:
```bash
python src/p2.api_request_parallel_processor.py \
  --requests_filepath data_sample/converted.jsonl \
  --save_filepath data_sample/embeddings.jsonl \
  --request_url https://api.openai.com/v1/embeddings \
  --max_requests_per_minute 1500 \
  --max_tokens_per_minute 6250000 \
  --token_encoding_name cl100k_base \
  --max_attempts 5 \
  --logging_level 20
```

#### p3
Converts the data to a csv, the required input type for the `p5.upload_to_pinecone.py` file

#### p4
Uploads it to pinecone

#### query
Just an example query to the pinecone index
