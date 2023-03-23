# Pinecone index filler

This implementation is largely reliant on the file `p3.api_request_parallel_processor.py`, which is an example provided in the OpenAI Playbook.

#### p1
generates the wholetext to vectorize, to make sure that the title is included in vectorization as well. right now the source url is included but that should change

#### p2 
converts the data to jsonl and appends a "job" to each datapoint, which is the required input for the `p3.api_request_parallel_processor.py`

#### p3
example provided by OpenAI, performs the assigned job (vectorization) on each article

#### p4
converts the data to a csv, the required input type for the `p5.upload_to_pinecone.py` file

#### p5
uploads it to pinecone

#### query
just an example query to the pinecone index