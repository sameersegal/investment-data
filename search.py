import yaml
import openai
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_embedding(text):
    response = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=text)
    return response["data"][0]["embedding"]


def main(collection: Collection, query: str):

    search_params = {
        "metric_type": "L2"
    }

    results = collection.search(
        data=[get_embedding(query)],  # Embeded search value
        anns_field="embeddings",  # Search across embeddings
        param=search_params,
        limit=5,  # Limit to five results per search
        output_fields=['id', 'title', 'url', 'body',
                       'date']  # Include title field in result
    )

    ret = []
    for hit in results[0]:
        row = []
        row.extend([
            hit.id,
            hit.score,
            hit.entity.get('title'),
            hit.entity.get('url'),
            hit.entity.get('date'),
            hit.entity.get('body')
        ])  # Get the id, distance, and title for the results
        ret.append(row)
    return ret

if __name__ == "__main__":
    connections.connect('default', host='localhost', port='19530')
    collection_name = 'malkauns'
    # dim = 1536  # The dimension of OpenAI embeddings
    # fields = [
    #     FieldSchema(name="id", dtype=DataType.INT64,
    #                 is_primary=True, auto_id=True),
    #     FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=100),
    #     FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=100),
    #     FieldSchema(name="date", dtype=DataType.VARCHAR, max_length=100),
    #     FieldSchema(name="body", dtype=DataType.VARCHAR, max_length=1000),
    #     FieldSchema(
    #         name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
    # ]
    # schema = CollectionSchema(
    #     fields, description="Stock Information")
    collection = Collection(collection_name)
    collection.load()
    query = "Elon Musk said XXXX about Telsa's long term growth"
    rows = main(collection, query)
    print(rows)
    connections.disconnect('default')
