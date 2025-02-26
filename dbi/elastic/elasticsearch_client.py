from elasticsearch import Elasticsearch
from datetime import datetime


class ElasticsearchClient:
    def __init__(self, host="http://localhost:9200"):
        # Connect to the Elasticsearch instance
        self.es = Elasticsearch(host, verify_certs=False)  # Disable SSL verification (for development purposes only)

        # Check if Elasticsearch is running
        if not self.es.ping():
            print("Elasticsearch is not running!")
        else:
            print("Connected to Elasticsearch")

        # Define the index name
        self.documents_index = "documents_index"

    def create_index(self):
        """Create the index with the custom mapping"""
        mapping = {
            "properties": {
                "type": {"type": "text"},
                "region": {"type": "text"},
                "category": {"type": "text"},
                "created_at": {"type": "date"},
                "total_sum": {"type": "float"},
                "doc_text": {"type": "text"}
            }
        }

        # Check if the index exists
        if self.es.indices.exists(index=self.documents_index):
            print(f"Index '{self.documents_index}' already exists!")
        else:
            # Create the index with the specified mapping
            self.es.indices.create(index=self.documents_index, body={"mappings": mapping})
            print(f"Index '{self.documents_index}' created!")

    def insert_document(self, doc_type, region, category, created_at, total_sum, doc_text):
        """Insert a document into the index"""
        doc = {
            "type": doc_type,
            "region": region,
            "category": category,
            "created_at": created_at,
            "total_sum": total_sum,
            "doc_text": doc_text
        }

        # Insert the document into Elasticsearch
        res = self.es.index(index=self.documents_index, document=doc)
        print(f"Document inserted: {res['_id']}")
        return res['_id']

    def get_document_by_id(self, doc_id):
        """Get a document by its ID"""
        try:
            res = self.es.get(index=self.documents_index, id=doc_id)
            print(f"Document retrieved: {res['_source']}")
        except Exception as e:
            print(f"Error retrieving document: {e}")

    def get_documents_by_field(self, field, value):
        """Get documents by a specific field (e.g., region)"""
        query = {
            "query": {
                "match": {
                    field: value
                }
            }
        }

        try:
            res = self.es.search(index=self.documents_index, body=query)
            print(f"Documents found: {len(res['hits']['hits'])}")
            for hit in res['hits']['hits']:
                print(f"Document ID: {hit['_id']} - Source: {hit['_source']}")
        except Exception as e:
            print(f"Error searching documents: {e}")


if __name__ == "__main__":
    client = ElasticsearchClient()
    # client.create_index()
    #
    # # Insert a document and capture its ID
    # doc_id = client.insert_document(
    #     doc_type="Invoice",
    #     region="North America",
    #     category="Finance",
    #     created_at=datetime.now().isoformat(),
    #     total_sum=1000.50,
    #     doc_text="This is a sample document with financial details."
    # )
    #
    # # Retrieve the document by ID
    # client.get_document_by_id(doc_id)

    # Search for documents by region
    print(client.get_documents_by_field("region", "North America"))
