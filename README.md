# HomeMatch - Personalized London Property Agent

> A LangChain-powered application that transforms standard London property listings into personalized narratives tailored to individual buyer preferences.

## 🏠 Project Overview

HomeMatch leverages Large Language Models (LLMs) and vector databases to create personalized London property experiences. The application interprets buyer preferences in natural language and matches them with relevant London properties, generating customized listing descriptions that highlight the most appealing aspects for each potential buyer in the London market.

## ✨ Features

- [ ] **Natural Language Preference Processing**: Interpret buyer requirements using LLMs
- [ ] **Semantic Property Search**: Vector-based matching of properties to preferences
- [ ] **Personalized Listing Generation**: Custom descriptions tailored to buyer interests
- [ ] **Multimodal Search** (Advanced): Image and text-based property matching using CLIP
- [ ] **Interactive Preference Collection**: User-friendly preference gathering interface

## 🛠️ Technology Stack

- **Framework**: LangChain
- **LLM Provider**: OpenAI GPT
- **Vector Database**: ChromaDB
- **Multimodal AI**: CLIP (Transformers, PyTorch)
- **Development**: Python 3.12, Poetry, Jupyter Notebooks

## 📋 Prerequisites

- Python 3.12+
- Poetry (for dependency management)
- OpenAI API Key

## 🚀 Installation

```bash
# Clone the repository
git clone <repository-url>
cd homematch

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Generate listings (Optional) - This will take a while
poetry run python src/data_generation/generate.py

# Generate embeddings from listings
poetry run python src/vector_store/store.py
```

## 📖 Usage

### Basic Usage

```python
# TODO: Add basic usage examples
```

### Running the Application

```bash
# TODO: Add instructions for running the main application
```

### Using the Conversational Interface

```bash
# Interactive property matching session
python src/preferences/matcher.py

# Demo with simulated responses
python src/preferences/demo.py
```

### Using Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open the main notebook
# TODO: Add notebook filename
```

## 📁 Project Structure

```
homematch/
├── data/                   # Generated listings and datasets
├── notebooks/              # Jupyter notebooks for development
├── src/                    # Source code
│   ├── __init__.py
│   ├── data_generation/    # LLM-based listing generation
│   ├── vector_store/       # Vector database operations
│   ├── search/             # Semantic search logic
│   └── personalization/    # Listing personalization
├── tests/                  # Test files
├── .env.example           # Environment variables template
├── pyproject.toml         # Poetry configuration
└── README.md              # This file
```

## 🏗️ Development Progress

### Step 1: Setting Up the Python Application
- [x] Initialize Poetry project
- [x] Configure dependencies
- [x] Set up development environment

### Step 2: Generating Real Estate Listings
- [x] Create LLM prompts for listing generation
- [x] Generate diverse property listings (minimum 10)

### Step 3: Storing Listings in Vector Database
- [x] Set up ChromaDB
- [x] Generate embeddings for listings
- [x] Store embeddings in vector database

### Step 4: Building User Preference Interface
- [x] Design preference collection questions
- [x] Implement preference parsing logic
- [x] Structure preferences for database queries

### Step 5: Searching Based on Preferences
- [x] Implement semantic search functionality
- [x] Fine-tune retrieval algorithms
- [x] Test search accuracy

### Step 6: Personalizing Listing Descriptions
- [ ] Develop LLM augmentation logic
- [ ] Ensure factual integrity preservation
- [ ] Test personalization quality

### Step 7: Testing and Validation
- [ ] Comprehensive application testing
- [ ] Multiple buyer preference scenarios
- [ ] Performance optimization

### Advanced Features (Optional)
- [ ] CLIP integration for multimodal search
- [ ] Image embedding generation
- [ ] Visual preference matching

## 🧪 Testing

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src
```

## 📊 Example Outputs

### Sample Conversational Flow
```
🤖 Hello! I'm your London property assistant. What type of property are you looking for?

👤 I'm looking for a flat, preferably modern

🤖 Great choice! How many bedrooms would you like, and what's your budget range?

👤 2 bedrooms would be ideal, and my budget is around £600k

🤖 Which areas of London interest you most?

👤 I'm interested in Clapham or Islington - somewhere trendy with good nightlife
```

### Sample Property Matches
```
🏠 Property 1 (Match: 72.3%)
📂 Category: Young Professionals
  • Price: £525,000
  • Bedrooms: 1
  • Size: 550 sqft
  • Location: Islington, N1
  📝 Preview: Stunning converted flat with modern features and excellent transport links...
```

## 🤝 Contributing

<!-- TODO: Add contribution guidelines if applicable -->

## 📝 License

<!-- TODO: Add license information -->

## 🔗 References

- [LangChain Documentation](https://langchain.readthedocs.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 📞 Contact

Mike Myat Min Han - mmhan@indeed.com

---

*This project is part of an AI upskilling initiative focused on practical applications of Large Language Models and Vector Databases.*