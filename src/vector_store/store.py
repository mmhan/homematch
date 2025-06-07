"""
London Property Vector Store Module
==================================

This module handles embedding generation and vector storage for London property listings.
It uses ChromaDB as the vector database and OpenAI embeddings for semantic search capabilities.
"""

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


@dataclass
class PropertyListing:
    """Structure for a property listing with metadata"""
    id: str
    category: str
    content: str


class PropertyVectorStore:
    """Manages the vector database for London property listings"""

    def __init__(self, persist_directory: str = "data/chroma_db"):
        """Initialize the vector store"""
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.vectorstore = None
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure the persist directory exists"""
        os.makedirs(self.persist_directory, exist_ok=True)

    def load_listings_from_json(self, json_file: str = "data/listings.json") -> List[PropertyListing]:
        """Load property listings from JSON file and convert to PropertyListing objects"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            listings = []
            for category, category_listings in raw_data.items():
                for i, listing_text in enumerate(category_listings):
                    # Generate unique ID for each listing
                    listing_id = f"{category}_{i}_{str(uuid.uuid4())[:8]}"

                    listing = PropertyListing(
                        id=listing_id,
                        category=category,
                        content=listing_text,
                    )
                    listings.append(listing)

            print(f"Loaded {len(listings)} property listings from {json_file}")
            return listings

        except FileNotFoundError:
            print(f"Error: {json_file} not found. Please generate listings first.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {json_file}")
            return []

    def create_documents(self, listings: List[PropertyListing]) -> List[Document]:
        """Convert PropertyListing objects to LangChain Documents with metadata"""
        documents = []

        for listing in listings:
            # Create metadata for filtering and search
            metadata = {
                "id": listing.id,
                "category": listing.category,
                "source": "generated_listings"
            }

            # Create document with full listing content
            doc = Document(
                page_content=listing.content,
                metadata=metadata
            )
            documents.append(doc)

        return documents

    def initialize_vectorstore(self, documents: List[Document]) -> None:
        """Initialize ChromaDB vector store with documents"""
        print("Creating embeddings and initializing vector store...")

        # Create ChromaDB vector store
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="london_properties"
        )

        print(f"Vector store initialized with {len(documents)} property listings")
        print(f"Persisted to: {self.persist_directory}")

    def load_existing_vectorstore(self) -> bool:
        """Load existing vector store if it exists"""
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="london_properties"
            )

            # Test if the collection has documents
            collection_count = self.vectorstore._collection.count()
            if collection_count > 0:
                print(f"Loaded existing vector store with {collection_count} documents")
                return True
            else:
                print("Existing vector store is empty")
                return False

        except Exception as e:
            print(f"Could not load existing vector store: {e}")
            return False

    def semantic_search(self, query: str, k: int = 5, filter_dict: Dict[str, Any] = None) -> List[Dict]:
        """Perform semantic search on property listings"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call setup_vectorstore() first.")

        # Perform similarity search
        if filter_dict:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k
            )

        # Format results
        formatted_results = []
        for doc, score in results:
            result = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": score
            }
            formatted_results.append(result)

        return formatted_results

    def setup_vectorstore(self, force_rebuild: bool = False) -> bool:
        """Main setup method - load or create vector store"""

        # Try to load existing vector store first
        if not force_rebuild and self.load_existing_vectorstore():
            return True

        print("Setting up new vector store...")

        # Load listings from JSON
        listings = self.load_listings_from_json()
        if not listings:
            print("No listings found. Cannot create vector store.")
            return False

        # Convert to documents
        documents = self.create_documents(listings)

        # Initialize vector store
        self.initialize_vectorstore(documents)

        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        if not self.vectorstore:
            return {"error": "Vector store not initialized"}

        try:
            total_docs = self.vectorstore._collection.count()

            return {
                "total_documents": total_docs,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main function to set up the vector store"""
    print("=== London Property Vector Store Setup ===")

    # Initialize vector store
    store = PropertyVectorStore()

    # Setup vector store (will load existing or create new)
    success = store.setup_vectorstore()

    if success:
        # Print statistics
        stats = store.get_stats()
        print("\n=== Vector Store Statistics ===")
        for key, value in stats.items():
            print(f"{key}: {value}")

        # Example search
        print("\n=== Example Search ===")
        query = "modern flat with good transport links"
        print(f"Query: {query}")
        results = store.semantic_search(query, k=3)

        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} (Score: {result['similarity_score']:.4f}) ---")
            print(f"Category: {result['metadata'].get('category', 'Unknown')}")
            print(f"Content preview: {result['content'][:200]}...")

    else:
        print("Failed to set up vector store")


if __name__ == "__main__":
    main()