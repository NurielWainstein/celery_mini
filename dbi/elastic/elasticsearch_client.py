from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from dbi.models.category import Category
from dbi.sql_connector import SessionLocal


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
                "region": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
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

    def get_documents_by_fields(self, fields_values):
        """Get documents by multiple fields and values (AND operator)"""
        # Build the query with a bool query and must conditions (AND operator)
        must_conditions = []
        for field, value in fields_values.items():
            must_conditions.append({
                "match": {
                    field: value
                }
            })

        query = {
            "query": {
                "bool": {
                    "must": must_conditions  # All conditions must be true (AND operator)
                }
            }
        }

        response = []
        try:
            q_res = self.es.search(index=self.documents_index, body=query)
            print(f"Documents found: {len(q_res['hits']['hits'])}")
            for hit in q_res['hits']['hits']:
                response.append({hit['_id']: hit['_source']})
                print(f"Document ID: {hit['_id']} - Source: {hit['_source']}")
        except Exception as e:
            print(f"Error searching documents: {e}")

        return response

    def find_regions(self, search_term, regions):
        """Return all regions that have at least one document containing the search term"""
        response = []
        try:
            # Use the 'terms' query to match any region in a single query
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"doc_text": search_term}},  # Match the search term in doc_text
                            {"terms": {"region.keyword": regions}}
                        ]
                    }
                },
                "size": 0,  # We don't need the actual documents, just the aggregation
                "aggs": {
                    "regions_with_matches": {
                        "terms": {
                            "field": "region.keyword",  # Use the 'keyword' subfield for aggregation
                            "size": len(regions)  # Limit aggregation to the number of regions
                        }
                    }
                }
            }

            # Search for documents matching the query
            q_res_check = self.es.search(index=self.documents_index, body=query)

            # Extract the regions from the aggregation results
            regions_with_matches = [bucket['key'] for bucket in
                                    q_res_check['aggregations']['regions_with_matches']['buckets']]

            # Prepare the response
            for region in regions_with_matches:
                response.append(region)

            print(f"Regions with documents containing search term '{search_term}': {response}")

        except Exception as e:
            print(f"Error searching documents: {e}")

        return response


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
    db: Session = SessionLocal()
    existing_regions = Category.get_unique_regions(db)

    print(client.find_regions("First", existing_regions))