from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import os


load_dotenv()

# Access environment variables
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

class Search:
    """
    A class for interacting with Elasticsearch index.
    """

    def __init__(self, index_name='psp_index', url=ELASTICSEARCH_URL,
                 username=ELASTICSEARCH_USERNAME, password=ELASTICSEARCH_PASSWORD):
        """
        Initialize the Search object.

        Parameters:
            index_name (str): Name of the Elasticsearch index.
            url (str): Elasticsearch URL.
            username (str): Username for Elasticsearch authentication.
            password (str): Password for Elasticsearch authentication.
        """
        self.es = Elasticsearch(url, http_auth=(username, password))
        self.index_name = index_name

    def create_index(self):
        """
        Create the Elasticsearch index.
        """
        if not self.index_exists():
            self.es.indices.create(index=self.index_name)
            print(f"Index '{self.index_name}' created.")
        else:
            print(f"Index '{self.index_name}' already exists.")

    def delete_index(self):
        """
        Delete the Elasticsearch index if it exists.
        """
        if self.index_exists():
            self.es.indices.delete(index=self.index_name)
            print(f"Index '{self.index_name}' deleted.")
        else:
            print(f"Index '{self.index_name}' does not exist.")

    def index_exists(self):
        """
        Check if the Elasticsearch index exists.

        Returns:
            bool: True if index exists, False otherwise.
        """
        return self.es.indices.exists(index=self.index_name)

    def insert_documents(self, documents):
        """
        Insert documents into the Elasticsearch index.

        Parameters:
            documents (list): List of documents to be inserted.
        """
        total_documents = len(documents)
        successful_inserts = 0
        actions = []
        for i, document in enumerate(documents, start=1):
            action = {
                "_index": self.index_name,
                "_id": document['sku'],
                "_source": document
            }
            actions.append(action)

            if len(actions) == 100 or i == total_documents:
                try:
                    success, _ = bulk(self.es, actions)
                    successful_inserts += success
                    actions = []  # Clear the actions list
                    print(f"{successful_inserts}/{total_documents} documents inserted.")
                except Exception as e:
                    print(f"Error inserting documents: {e}")

        print(f"All documents inserted. Successful inserts: {successful_inserts}/{total_documents}")

    def count_documents(self):
        """
        Count the number of documents in the Elasticsearch index.

        Returns:
            int: Number of documents in the index.
        """
        try:
            response = self.es.count(index=self.index_name)
            count = response['count']
            print(f"Number of documents in index '{self.index_name}': {count}")
            return count
        except Exception as e:
            print(f"Error counting documents: {e}")
            return -1

    def add_more_documents(self, file_path):
        """
        Add more documents to the Elasticsearch index.

        Parameters:
            file_path (str): Path to the file containing additional documents.
        """
        if not self.index_exists():
            print(f"Index '{self.index_name}' does not exist. Please create the index first.")
            return

        try:
            with open(file_path, 'rt') as f:
                documents = json.load(f)
                self.insert_documents(documents)
        except Exception as e:
            print(f"Error adding more documents: {e}")

    def search_documents(self, query):
        """
        Search documents in the Elasticsearch index.

        Parameters:
            query (str): Search query.

        Returns:
            list: List of search results.
        """
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["name^2", "categories", "description^2", "sort_description","country_of_manufacture"],
                    "type": "cross_fields"
                }
            }
        }
        try:
            response = self.es.search(index=self.index_name, body=search_body)
            hits = response['hits']['hits']
            results = []
            for hit in hits:
                source = hit['_source']
                result = {
                    'sku': source['sku'],
                    'name': source['name'],
                    'description': source['description'],
                    'short_description' : source['short_description'],
                    'price': source['price'],
                    'special_price': source['special_price'],
                    'country_of_manufacture' : source['country_of_manufacture'],
                    'categories': source['categories'],
                    'score': hit['_score']
                }
                results.append(result)
            return results
        except Exception as e:
            print(f"Error executing search query: {e}")
            return []

