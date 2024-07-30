import pandas as pd
from pymongo.mongo_client import MongoClient
import json
from typing import Any

class MongoOperation:
    __collection = None
    __database = None

    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_mongo_client(self) -> MongoClient:
        return MongoClient(self.client_url)

    def create_database(self) -> Any:
        if MongoOperation.__database is None:
            client = self.create_mongo_client()
            MongoOperation.__database = client[self.database_name]
        return MongoOperation.__database

    def create_collection(self, collection_name: str = None) -> Any:
        if collection_name:
            self.collection_name = collection_name

        if (MongoOperation.__collection is None or
                MongoOperation.__collection != self.collection_name):
            database = self.create_database()
            MongoOperation.__collection = database[self.collection_name]

        return MongoOperation.__collection

    def insert_record(self, record: dict, collection_name: str) -> None:
        collection = self.create_collection(collection_name)
        if isinstance(record, list):
            if not all(isinstance(data, dict) for data in record):
                raise TypeError("All records must be dictionaries")
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection.insert_one(record)
        else:
            raise TypeError("Record must be a dictionary or list of dictionaries")

    def bulk_insert(self, datafile: str, collection_name: str = None) -> None:
        if collection_name:
            self.collection_name = collection_name

        if datafile.endswith('.csv'):
            dataframe = pd.read_csv(datafile, encoding='utf-8')
        elif datafile.endswith(".xlsx"):
            dataframe = pd.read_excel(datafile, encoding='utf-8')
        else:
            raise ValueError("Unsupported file format")

        datajson = json.loads(dataframe.to_json(orient='records'))
        collection = self.create_collection()
        collection.insert_many(datajson)
