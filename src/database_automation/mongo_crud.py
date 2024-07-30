import pandas as pd
from pymongo.mongo_client import MongoClient
import json

class MongoOperation:
    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name
        self.__database = None
        self.__collection = None

    def create_mongo_client(self) -> MongoClient:
        return MongoClient(self.client_url)

    def create_database(self):
        if self.__database is None:
            client = self.create_mongo_client()
            self.__database = client[self.database_name]
        return self.__database

    def create_collection(self):
        if self.__collection is None and self.collection_name:
            database = self.create_database()
            self.__collection = database[self.collection_name]
        return self.__collection

    def insert_record(self, record: dict, collection_name: str):
        collection = self.create_collection()
        if isinstance(record, list):
            for data in record:
                if not isinstance(data, dict):
                    raise TypeError("Record must be a dict")
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection.insert_one(record)

    def bulk_insert(self, datafile: str):
        if datafile.endswith('.csv'):
            dataframe = pd.read_csv(datafile, encoding='utf-8')
        elif datafile.endswith('.xlsx'):
            dataframe = pd.read_excel(datafile, encoding='utf-8')
        else:
            raise ValueError("Unsupported file type")

        datajson = json.loads(dataframe.to_json(orient='records'))
        collection = self.create_collection()
        collection.insert_many(datajson)
