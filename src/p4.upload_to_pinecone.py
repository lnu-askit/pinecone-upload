import pinecone
import csv
import numpy as np
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

"""
This class is largely copy pasted from a pinecone example
"""

class PineconeUpload:
    def __init__(
        self,
        pinecone_api_key,
        index_name,
        embeddings_csv,
        embedding_dims: 1536,
        create_index: bool = False,
    ) -> None:
        self.pinecone_api_key = pinecone_api_key
        self.index_name = index_name
        self.embeddings_csv = embeddings_csv
        self.embedding_dims = embedding_dims
        self.create_index = create_index
        self.pinecone_index = self.make_pinecone_index()

    def get_first_4000_chars(self, s):
        """
        Recommended splitting from Pinecone, metadata has some sort of inconsistent filesize cap.
        """
        if len(s) > 4000:
            return s[:4000]
        else:
            return s

    def make_pinecone_index(self):        
        pinecone.init(api_key=self.pinecone_api_key, environment=os.environ.get('PINECONE_ENV'))
        
        if self.create_index:
            # Create an empty index if required (i made mine manually instead)
            pinecone.create_index(name=self.index_name, dimension=self.embedding_dims)
        
        index = pinecone.Index(self.index_name)

        print(f"Pinecone index info: {pinecone.whoami()} \n")
        return index

    def upsert_embeddings_batch(self, starting_index, data_batch, index_offset):
        """Define a function to upsert embeddings in batches."""

        upsert_requests = [
            (
                str(starting_index + i + index_offset),
                embedding,
                {"text": self.get_first_4000_chars(row[0])},
            )  # taking 1500 first characters because of meta size limit
            for i, row in enumerate(data_batch)
            for embedding in [np.array([float(x) for x in row[1:]]).tolist()]
        ]

        # Upsert the embeddings in batch
        upsert_response = self.pinecone_index.upsert(vectors=upsert_requests, namespace="articles")

        return upsert_response

    def upsert_embeddings_to_index(self):
        with open(self.embeddings_csv, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            data = list(reader)

        batch_size = 100
        index_offset = 0
        while index_offset < len(data):
            batch = data[index_offset : index_offset + batch_size]

            self.upsert_embeddings_batch(0, batch, index_offset)
            print("batch " + str(index_offset))
            index_offset += batch_size
        print(f"Total vectors in the index: {self.pinecone_index.describe_index_stats()['total_vector_count']}")


if __name__ == "__main__":
    dotenv_path = join(dirname(__file__), '.env')
    info = load_dotenv(dotenv_path)

    index_name = "serviceportalenlnu"
    embeddings_csv = "data_sample/embeddings.csv"
    embedding_dims = 1536
    create_index = False # I made a manual index instead, something keeps going wrong making it dynamically


    pinecone = PineconeUpload(
        pinecone_api_key=os.environ.get('PINECONE_API_KEY'),
        index_name=index_name,
        embeddings_csv=embeddings_csv,
        embedding_dims=embedding_dims,
        create_index=create_index,
    )

    pinecone.upsert_embeddings_to_index()