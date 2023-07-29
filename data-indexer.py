# Index all files in the output directory into Milvus vector database

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


def main(collection: Collection, path: str):

    for f in os.listdir(path):
        if not f.endswith(".yml"):
            continue

        print(f"Processing {f}")
        with open(os.path.join(path, f), 'r') as file:
            content = file.read()
            yaml_data = yaml.load(content, Loader=yaml.FullLoader)
            title = yaml_data['title']
            body = yaml_data['body']
            url = yaml_data['url']
            date = yaml_data['date']

            c = 0
            ids = []
            titles = []
            bodys = []
            urls = []
            dates = []
            embeddings = []

            for i in range(0, len(body), 1000):
                text = body[i:i+1000]
                embedding = get_embedding(text)

                ids += [f"{f}-{c}"]
                titles += [title]
                bodys += [text]
                urls += [url]
                dates += [str(date)]
                embeddings += [embedding]

                c += 1

            entities = [ids, titles, urls, dates, bodys, embeddings]
            # print(entities)
            collection.insert(entities)
            collection.flush()
        break


if __name__ == "__main__":
    directory = os.path.join(os.getcwd(), 'output')
    connections.connect("default",
                        host="localhost", port="19530")

    collection_name = "malkauns"
    utility.drop_collection(collection_name)
    # if not utility.has_collection(collection_name):
    dim = 1536  # The dimension of OpenAI embeddings
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=100,
                    is_primary=True),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="date", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="body", dtype=DataType.VARCHAR, max_length=1010),
        FieldSchema(
            name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    schema = CollectionSchema(
        fields, description="Stock Information")
    collection = Collection(collection_name, schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128}
    }
    collection.create_index("embeddings", index_params)

    # client.create_collection(collection)

    # client.load_collection(collection)

    main(collection, directory)

    connections.disconnect("default")
