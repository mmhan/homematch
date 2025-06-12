# HomeMatch - Personalized London Property Agent

> A LangChain-powered application that transforms standard London property listings into personalized narratives tailored to individual buyer preferences.

## 🏠 Project Overview

HomeMatch leverages Large Language Models (LLMs) and vector databases to create personalized London property experiences. The application interprets buyer preferences in natural language and matches them with relevant London properties, generating customized listing descriptions that highlight the most appealing aspects for each potential buyer in the London market.

## ✨ Features

- [x] **Natural Language Preference Processing**: Interpret buyer requirements using LLMs
- [x] **Semantic Property Search**: Vector-based matching of properties to preferences
- [x] **Personalized Listing Generation**: Custom descriptions tailored to buyer interests
- [x] **Interactive Preference Collection**: Conversational agent for gathering buyer preferences
- [x] **Multi-Persona Demo System**: Pre-built personas for testing different buyer types

## 🛠️ Technology Stack

- **Framework**: LangChain
- **LLM Provider**: OpenAI GPT-4o-mini
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embeddings
- **Development**: Python 3.12, Poetry

## 📋 Prerequisites

- Python 3.12+
- Poetry (for dependency management)
- OpenAI API Key

## 🚀 Installation

```bash
cd homematch

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Set up environment variables
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and OPENAI_BASE_URL

# Generate sample listings (Optional - takes ~5 minutes)
python src/data_generation/generate.py

# Set up vector database with embeddings
python src/vector_store/store.py
```

## 📖 Usage

### Quick Demo

```bash
# Run the comprehensive demo with all personas
python src/demo.py
```

### Using Pre-built Personas

```python
from src.demo import DemoRunner

demo = DemoRunner()

# Run a specific persona (e.g., Young Professional)
persona_responses = demo.get_persona_responses()
demo.run_persona_demo("Young Professionals", persona_responses["Young Professionals"])
```

## 🎭 Built-in Buyer Personas

The system includes 6 pre-configured London buyer personas:

1. **Family Areas** - Looking for family homes in Richmond/Wimbledon
2. **Young Professionals** - Modern flats in trendy areas like Clapham/Shoreditch
3. **Luxury Central** - Premium properties in Kensington/Chelsea/Mayfair
4. **Up and Coming Areas** - Value properties in developing areas like Peckham
5. **First Time Buyer** - Affordable options in outer London zones
6. **Unique London Properties** - Distinctive properties like warehouse conversions

## 📁 Project Structure

```
homematch/
├── data/                    # Generated listings and vector database
│   ├── listings.json       # 24 synthetic London property listings
│   └── chroma_db/          # ChromaDB vector storage
├── src/                    # Source code
│   ├── data_generation/    # LLM-based listing generation
│   │   └── generate.py     # Property listing generator
│   ├── vector_store/       # Vector database operations
│   │   └── store.py        # ChromaDB integration & semantic search
│   ├── search/             # Preference collection & search
│   │   └── search.py       # Conversational preference collector
│   ├── personalization/    # Listing personalization
│   │   └── personalize.py  # LLM-based description personalization
│   └── demo.py            # Multi-persona demo system
├── .env.example           # Environment variables template
├── pyproject.toml         # Poetry configuration
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run the demo system
python src/demo.py

# Test individual components
python src/vector_store/store.py
python src/search/search.py
python src/personalization/personalize.py
```

## 📊 Example Output

```
❯ python src/demo.py
🏠 Homematch Demo
=====================================
Loaded existing vector store with 24 documents

Choose a demo option:
1. Run all persona demos
2. Family Areas persona
3. Young Professionals persona
4. Luxury Central persona
5. Up and Coming Areas persona
6. First Time Buyer persona
7. Unique London Properties persona
8. Interactive demo (your own preferences)
9. Exit

Enter your choice (1-9): 5

============================================================
🏠 DEMO: UP AND COMING AREAS PERSONA
============================================================
🤖 Assistant: Hello! I'm here to help you find your perfect London property.

I'll ask you a few questions about your preferences to understand what you're looking for. This should take about 2-3 minutes.

Let's start! What type of property are you looking for?

Options include: terraced house, semi-detached house, detached house, flat, studio flat, 1-bed flat, shared ownership, new build apartment, conversion, loft apartment, period house, or something else?

👤 User: Victorian conversion or terraced house

🤖 Assistant: Great! What's your budget range?

👤 User: £400,000 to £650,000

🤖 Assistant: How many bedrooms do you need? Any flexibility on this?

👤 User: 2-3 bedrooms

🤖 Assistant: Any preference on bathrooms? Is an en-suite important?

👤 User: 1-2 bathrooms

🤖 Assistant: Do you need outdoor space? Garden, balcony, or roof terrace?

👤 User: Small garden or courtyard would be great

🤖 Assistant: Are there specific areas in London you're interested in or want to avoid?

👤 User: Peckham, Forest Hill, or Walthamstow

🤖 Assistant: Where do you need to commute to for work? And what's your acceptable commute time?

👤 User: Central London, up to 45 minutes is okay

🤖 Assistant: Do you prefer tube, bus, rail, or are you flexible with transport? How important are direct transport links?

👤 User: Good transport links, Overground or tube

🤖 Assistant: What's important to have nearby: shops, restaurants, parks, gyms, schools? Do you prefer busy areas with nightlife or quieter residential areas?

👤 User: Local cafes, markets, developing arts scene

🤖 Assistant: Do you prefer established family neighborhoods, trendy up-and-coming areas, or central locations?

👤 User: Up-and-coming areas with potential

🤖 Assistant: Any must-have features (parking, period features, modern kitchen, etc.) or deal-breakers? Any special requirements?

👤 User: Character features, potential for improvement

🤖 Assistant: If you had to choose, what are your top 3 most important factors from everything we've discussed?

👤 User: Good transport, value for money, character

🤖 Assistant: Let me confirm what I've understood about your preferences:

• Property type: Victorian conversion or terraced house
• Budget: £400,000 to £650,000
• Bedrooms: 2-3 bedrooms
• Bathrooms: 1-2 bathrooms
• Outdoor space: Small garden or courtyard would be great
• Preferred areas: Peckham, Forest Hill, or Walthamstow
• Commute: Central London, up to 45 minutes is okay
• Transport: Good transport links, Overground or tube
• Amenities: Local cafes, markets, developing arts scene
• Community type: Up-and-coming areas with potential
• Features: Character features, potential for improvement
• Top priorities: Good transport, value for money, character

Is this correct? If there's anything else important I should know about your ideal property, please let me know.

👤 User: Yes, that captures what I want

🤖 Assistant: Perfect! I'll now generate your property search query.

🔍 Generated Semantic Query:
   "Victorian conversion or terraced house in Peckham, Forest Hill, or Walthamstow with 2-3 bedrooms and 1-2 bathrooms, featuring a small garden or courtyard, within a budget of £400,000 to £650,000. Must have character features and potential for improvement, located in an up-and-coming area with good transport links to Central London (up to 45 minutes commute), and close to local cafes, markets, and a developing arts scene."

🔍 Searching vector database...

🎯 PERSONALIZED PROPERTY RECOMMENDATIONS
Found 1 properties tailored to your preferences

RECOMMENDATION #1
============================================================
🏠 PERSONALIZED LISTING
📊 Match Score: 0.2254
============================================================
✨ WHY THIS MATCHES YOUR PREFERENCES:
   • Bedroom Requirements: 2-3 bedrooms
   • Outdoor Space Available
   • Preferred Location: Peckham, Forest Hill, or Walthamstow
   • Good Transport Links
   • Desired Amenities: local

📝 PERSONALIZED DESCRIPTION:
**Personalized Property Listing: Charming Victorian Conversion in Up-and-Coming Peckham**

**Basic Info:**
- **Area/Postcode:** Peckham, SE15
- **Price:** £475,000
- **Bedrooms:** 2
- **Bathrooms:** 1
- **Size:** 750 sqft
- **Property Type:** Victorian Conversion Flat

---

**Property Description:**
Welcome to your future home nestled in the vibrant heart of Peckham! This delightful two-bedroom Victorian conversion flat combines character, charm, and exceptional potential—all within your budget and ideal location. Spanning a generous 750 sqft, this property features high ceilings with original cornicing and large sash windows that flood the space with natural light, creating an inviting atmosphere for both relaxation and entertaining.

The open-plan living area is perfect for your lifestyle, seamlessly blending a contemporary kitchen with traditional features, making it the ideal backdrop for hosting friends or enjoying cozy nights in. Both bedrooms are well-proportioned, offering versatility for guests or a home office, while the master bedroom boasts a decorative fireplace that adds an elegant touch, enhancing the character you desire.

The stylish bathroom is fitted with modern fixtures while preserving the property’s period charm, ensuring you feel at home from day one. Step outside to the tranquil rear garden, a lovely spot for your morning coffees or evening relaxation, adding that essential outdoor space you've been looking for.

This flat is a fantastic choice for first-time buyers or investors eager to tap into the potential of this up-and-coming area. With its character features and space for improvement, it offers the perfect canvas for you to create your dream home.

---

**Area Description:**
Peckham is rapidly emerging as one of South London's most desirable neighborhoods, renowned for its eclectic mix of cultural offerings and a strong community vibe. With excellent transport links, including frequent Overground services from Peckham Rye station that connect you to London Bridge in under 15 minutes, commuting to Central London is a breeze—perfect for your lifestyle needs!

You'll love the array of local amenities at your doorstep, from the picturesque Peckham Rye Park to the bustling Peckham Levels, home to independent shops, trendy eateries, and art spaces that reflect the developing arts scene you seek. The nearby Bellenden Road and iconic Market are ideal for weekend strolls, featuring artisan coffee shops and inviting pubs, contributing to the vibrant community atmosphere.

This property not only meets your requirements but places you in an area bursting with potential, value for money, and a warm, welcoming spirit. Don’t miss out on this opportunity to invest in your future in a neighborhood that’s on the rise—your charming Victorian conversion in Peckham awaits!
```

## 🎮 Demo Options

Run `python src/demo.py` and choose from:

1. **Run all persona demos** - See all 6 buyer types in action
2. **Individual persona demos** - Test specific buyer scenarios
3. **Interactive demo** - Input your own preferences live
4. **Exit** - Close the application

Each demo shows the complete flow: preference collection → semantic search → personalized recommendations.
