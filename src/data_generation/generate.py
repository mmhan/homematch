import os
import json
import random

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

categories: dict[str, dict] = {
    "family_areas": {
        "description": "2-4 bedrooms in family-friendly areas - good schools, parks, family pubs",
        "locations": ["Richmond", "Wimbledon", "Greenwich", "Barnes"],
        "property_types": ["terraced house", "semi-detached house", "family flat", "Victorian house"]
    },
    "young_professionals": {
        "description": "1-2 bed flats for young professionals - with tube access, nightlife, and/or cafes",
        "locations": ["Clapham", "Islington", "Shoreditch", "Brixton"],
        "property_types": ["modern flat", "converted flat", "studio apartment", "new build apartment"]
    },
    "luxury_central": {
        "description": "Premium flats/houses - period features, or prime locations",
        "locations": ["Kensington", "Marylebone", "Mayfair", "Chelsea"],
        "property_types": ["period apartment", "penthouse", "Georgian house", "luxury flat"]
    },
    "up_and_coming": {
        "description": "Value properties in developing areas - with good transport, developing areas",
        "locations": ["Peckham", "Forest Hill", "Walthamstow", "New Cross"],
        "property_types": ["Victorian conversion", "terraced house", "purpose-built flat", "ex-council flat"]
    },
    "first_time_buyer": {
        "description": "Studio/1-bed in London zones 3-4, with shared ownership, or Help to Buy eligible",
        "locations": ["Croydon", "Woolwich", "Barking", "Walthamstow"],
        "property_types": ["studio flat", "1-bed flat", "shared ownership", "new build apartment"]
    },
    "unique_london_properties": {
        "description": "Unique and distinctive properties",
        "locations": ["King's Cross", "Canary Wharf", "Bermondsey", "Hackney Wick"],
        "property_types": ["warehouse conversion", "canal-side flat", "loft apartment", "period house"]
    },
}

def prompt_template(category: str, variation_instruction: str = "") -> str:
    return PromptTemplate.from_template(
        """
        You are a real estate agent in London.

        Generate a realistic London property listing for the "{category}" category.

        The category could be described as:
        {description}

        {variation_instruction}

        The listing should contain the following sections:

        Basic Info: area/postcode, price (£), bedrooms, bathrooms, size (sqft), property type
        Property Description: 150-200 words, highlight unique features and period details
        Area Description: 100-150 words, transport links, local amenities, community vibe

        Constraints:
        - Realistic London pricing for the area and property type
        - Include transport connections (tube lines, bus routes, rail stations)
        - Mention specific London amenities (parks, markets, pubs, cultural attractions)
        - Rich descriptive language optimized for semantic search
        - Make each listing unique with different features, prices, and characteristics
        """
    ).format(
        category=category,
        description=categories[category]["description"],
        variation_instruction=variation_instruction
    )

def generate_listing_for_category(category: str, location: str = None, property_type: str = None) -> str:
    # Select specific location and property type if not provided
    if location is None:
        location = random.choice(categories[category]["locations"])
    if property_type is None:
        property_type = random.choice(categories[category]["property_types"])

    variation_instruction = f"IMPORTANT: This listing must be specifically located in {location} and must be a {property_type}. Use this specific area and property type throughout the listing."

    prompt = prompt_template(category, variation_instruction)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.8,  # Increased temperature for more variation
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    response = llm.invoke(prompt)
    return response.content

def generate_listings_for_category(category: str, count: int = 4) -> list[str]:
    listings = []
    locations = categories[category]["locations"].copy()
    property_types = categories[category]["property_types"].copy()

    # Shuffle to add randomness
    random.shuffle(locations)
    random.shuffle(property_types)

    # Ensure we get variety by cycling through locations and property types
    for i in range(count):
        # Rotate through locations to ensure variety
        location = locations[i % len(locations)]
        property_type = property_types[i % len(property_types)]

        print(f"Generating {category} listing {i+1}/{count}: {location} - {property_type}")
        listing = generate_listing_for_category(category, location, property_type)
        listings.append(listing)

    return listings

def generate_listings():
    listings = {}
    for category in categories:
        listings[category] = generate_listings_for_category(category)
    return listings


def save_listings(listings: dict[str, list[str]], filename: str):
    with open(filename, "w") as f:
        json.dump(listings, f, indent=2)

def main():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    print("Starting listing generation...")
    listings = generate_listings()
    save_listings(listings, "data/listings.json")
    print(f"Generated {sum(len(category_listings) for category_listings in listings.values())} listings saved to data/listings.json")


if __name__ == "__main__":
    main()