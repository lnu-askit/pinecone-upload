import openai
import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key=os.environ.get('OPENAI_API_KEY')

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),
    environment=os.environ.get('PINECONE_ENV')  # find next to API key in console
)

# connect to index
index = pinecone.Index('serviceportalenlnu')
print(f"Pinecone index info: {pinecone.whoami()} \n")

MODEL="text-embedding-ada-002"

query = ""

xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
#print(xq)

res = index.query([xq], top_k=5, include_metadata=True, namespace="articles")
print('question: ' + query)
print(res )