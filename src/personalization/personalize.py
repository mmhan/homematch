"""
Personalized Listing Description Generator
==========================================

This module takes search results from the vector store and buyer preferences
to generate personalized property listing descriptions that highlight aspects
most relevant to the buyer while maintaining factual integrity.
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Import from our existing modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from search.search import BuyerPreferences

# Load environment variables from .env file
load_dotenv()


@dataclass
class PersonalizedListing:
    """Data class for a personalized listing result"""
    original_content: str
    personalized_description: str
    category: str
    similarity_score: float
    preference_highlights: List[str]
    metadata: Dict[str, Any]


class ListingPersonalizer:
    """Generates personalized listing descriptions based on buyer preferences"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,  # Slightly higher for creative personalization
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    def personalize_listings(
        self,
        search_results: List[Dict[str, Any]],
        buyer_preferences: BuyerPreferences
    ) -> List[PersonalizedListing]:
        """
        Generate personalized descriptions for search results based on buyer preferences

        Args:
            search_results: Results from vector store semantic search
            buyer_preferences: Collected buyer preferences

        Returns:
            List of PersonalizedListing objects with tailored descriptions
        """
        personalized_listings = []

        # Extract key preference themes for personalization
        preference_context = self._extract_preference_context(buyer_preferences)

        for result in search_results:
            try:
                personalized_description = self._generate_personalized_description(
                    original_content=result['content'],
                    preferences=buyer_preferences,
                    preference_context=preference_context,
                    category=result['metadata'].get('category', 'Unknown')
                )

                # Extract highlighted preference matches
                highlights = self._identify_preference_highlights(
                    result['content'],
                    buyer_preferences
                )

                personalized_listing = PersonalizedListing(
                    original_content=result['content'],
                    personalized_description=personalized_description,
                    category=result['metadata'].get('category', 'Unknown'),
                    similarity_score=result['similarity_score'],
                    preference_highlights=highlights,
                    metadata=result['metadata']
                )

                personalized_listings.append(personalized_listing)

            except Exception as e:
                print(f"Warning: Could not personalize listing - {e}")
                # Fallback to original content if personalization fails
                fallback_listing = PersonalizedListing(
                    original_content=result['content'],
                    personalized_description=result['content'],
                    category=result['metadata'].get('category', 'Unknown'),
                    similarity_score=result['similarity_score'],
                    preference_highlights=[],
                    metadata=result['metadata']
                )
                personalized_listings.append(fallback_listing)

        return personalized_listings

    def _extract_preference_context(self, preferences: BuyerPreferences) -> Dict[str, str]:
        """Extract and categorize key preference themes for personalization"""
        context = {
            "property_focus": preferences.property_type,
            "budget_context": preferences.budget_range,
            "location_priorities": preferences.preferred_areas,
            "amenity_priorities": preferences.amenities,
            "transport_priorities": preferences.transport_preference,
            "feature_priorities": preferences.must_have_features,
            "top_priorities": preferences.top_priorities
        }

        return context

    def _generate_personalized_description(
        self,
        original_content: str,
        preferences: BuyerPreferences,
        preference_context: Dict[str, str],
        category: str
    ) -> str:
        """Generate a personalized description using LLM"""

        personalization_prompt = PromptTemplate.from_template(
            """You are a skilled real estate agent writing a personalized property description for a specific buyer.

ORIGINAL LISTING:
{original_content}

BUYER PREFERENCES:
- Property Type: {property_type}
- Budget: {budget_range}
- Bedrooms: {bedrooms}
- Bathrooms: {bathrooms}
- Outdoor Space Needs: {outdoor_space}
- Preferred Areas: {preferred_areas}
- Commute Requirements: {commute_location}
- Transport Preferences: {transport_preference}
- Important Amenities: {amenities}
- Community Type: {community_type}
- Must-Have Features: {must_have_features}
- Top Priorities: {top_priorities}

PERSONALIZATION GUIDELINES:
1. MAINTAIN ALL FACTUAL INFORMATION: Keep all prices, addresses, sizes, and factual details exactly as they are
2. EMPHASIZE RELEVANT ASPECTS: Highlight features that match the buyer's stated preferences
3. USE BUYER'S LANGUAGE: Reference their specific needs and priorities in the description
4. CONNECT TO LIFESTYLE: Show how the property fits their lifestyle and requirements
5. HIGHLIGHT MATCHES: Draw attention to elements that align with their top priorities
6. MAINTAIN PROFESSIONAL TONE: Keep the description engaging but professional

 PERSONALIZATION FOCUS:
 - Property category: {category}
 - Location priorities: {location_priorities}
 - Feature priorities: {feature_priorities}

 Write a personalized version of the listing that speaks directly to this buyer's needs while maintaining all factual accuracy. Make them excited about how this property could be perfect for them.

PERSONALIZED LISTING:"""
        )

        # Generate the personalized description
        chain = personalization_prompt | self.llm | StrOutputParser()

        personalized_content = chain.invoke({
            "original_content": original_content,
            "property_type": preferences.property_type,
            "budget_range": preferences.budget_range,
            "bedrooms": preferences.bedrooms,
            "bathrooms": preferences.bathrooms,
            "outdoor_space": preferences.outdoor_space,
            "preferred_areas": preferences.preferred_areas,
            "commute_location": preferences.commute_location,
            "transport_preference": preferences.transport_preference,
            "amenities": preferences.amenities,
            "community_type": preferences.community_type,
            "must_have_features": preferences.must_have_features,
            "top_priorities": preferences.top_priorities,
            "category": category,
            "location_priorities": preference_context.get("location_priorities", ""),
            "feature_priorities": preference_context.get("feature_priorities", "")
        })

        return personalized_content.strip()

    def _identify_preference_highlights(
        self,
        original_content: str,
        preferences: BuyerPreferences
    ) -> List[str]:
        """Identify which buyer preferences are highlighted in the listing"""
        highlights = []
        content_lower = original_content.lower()

        # Check for property type matches
        if preferences.property_type and preferences.property_type.lower() in content_lower:
            highlights.append(f"Property Type: {preferences.property_type}")

        # Check for bedroom/bathroom mentions
        if preferences.bedrooms:
            bedroom_keywords = ["bedroom", "bed"]
            if any(keyword in content_lower for keyword in bedroom_keywords):
                highlights.append(f"Bedroom Requirements: {preferences.bedrooms}")

        # Check for outdoor space mentions
        if preferences.outdoor_space and preferences.outdoor_space.lower() != "no":
            outdoor_keywords = ["garden", "balcony", "terrace", "outdoor", "patio"]
            if any(keyword in content_lower for keyword in outdoor_keywords):
                highlights.append("Outdoor Space Available")

        # Check for area mentions
        if preferences.preferred_areas:
            area_words = preferences.preferred_areas.lower().split()
            if any(word in content_lower for word in area_words if len(word) > 3):
                highlights.append(f"Preferred Location: {preferences.preferred_areas}")

        # Check for transport mentions
        if preferences.transport_preference:
            transport_keywords = ["tube", "station", "transport", "bus", "rail", "line"]
            if any(keyword in content_lower for keyword in transport_keywords):
                highlights.append("Good Transport Links")

        # Check for amenity mentions
        if preferences.amenities:
            amenity_words = preferences.amenities.lower().split()
            matched_amenities = [word for word in amenity_words if word in content_lower and len(word) > 3]
            if matched_amenities:
                highlights.append(f"Desired Amenities: {', '.join(matched_amenities[:3])}")

        return highlights

    def format_personalized_listing(self, listing: PersonalizedListing) -> str:
        """Format a personalized listing for display"""
        output = []
        output.append("=" * 60)
        output.append(f"🏠 PERSONALIZED LISTING")
        output.append(f"📊 Match Score: {listing.similarity_score:.4f}")
        output.append("=" * 60)

        if listing.preference_highlights:
            output.append("✨ WHY THIS MATCHES YOUR PREFERENCES:")
            for highlight in listing.preference_highlights:
                output.append(f"   • {highlight}")
            output.append("")

        output.append("📝 PERSONALIZED DESCRIPTION:")
        output.append(listing.personalized_description)
        output.append("")

        return "\n".join(output)

    def display_personalized_results(self, personalized_listings: List[PersonalizedListing]) -> None:
        """Display all personalized listings in a formatted way"""
        print(f"\n🎯 PERSONALIZED PROPERTY RECOMMENDATIONS")
        print(f"Found {len(personalized_listings)} properties tailored to your preferences\n")

        for i, listing in enumerate(personalized_listings, 1):
            print(f"RECOMMENDATION #{i}")
            print(self.format_personalized_listing(listing))
            if i < len(personalized_listings):
                print("\n" + "-" * 60 + "\n")


# Convenience function for easy integration
def personalize_search_results(
    search_results: List[Dict[str, Any]],
    buyer_preferences: BuyerPreferences
) -> List[PersonalizedListing]:
    """
    Convenience function to personalize search results

    Args:
        search_results: Results from vector store semantic search
        buyer_preferences: Collected buyer preferences

    Returns:
        List of PersonalizedListing objects
    """
    personalizer = ListingPersonalizer()
    return personalizer.personalize_listings(search_results, buyer_preferences)


# Demo function for testing
def demo_personalization():
    """Demo function to test personalization functionality"""
    from search.search import PropertyPreferenceCollector, BuyerPreferences
    from vector_store.store import PropertyVectorStore

    print("🏠 Personalization Demo")
    print("=" * 40)

    # Example buyer preferences
    preferences = BuyerPreferences(
         property_type="modern flat",
         budget_range="£450,000 to £550,000",
         bedrooms="1-2 bedrooms",
         bathrooms="1 bathroom",
         outdoor_space="balcony would be nice",
         preferred_areas="Clapham, Islington, or Shoreditch",
         commute_location="Central London",
         transport_preference="tube access essential",
         amenities="cafes, restaurants, nightlife, gyms",
         community_type="trendy areas with nightlife",
         must_have_features="modern kitchen, secure building",
         top_priorities="transport links, nightlife, modern amenities"
     )

    try:
        # Initialize vector store
        store = PropertyVectorStore()
        store.setup_vectorstore()

        # Perform search
        query = "Modern 1-2 bedroom flat in trendy area with tube access, nightlife, and modern amenities"
        search_results = store.semantic_search(query, k=1)

        if search_results:
            # Personalize results
            personalizer = ListingPersonalizer()
            personalized = personalizer.personalize_listings(search_results, preferences)

            # Display results
            personalizer.display_personalized_results(personalized)
        else:
            print("No search results found for personalization demo")

    except Exception as e:
        print(f"Demo error: {e}")


if __name__ == "__main__":
    demo_personalization()
