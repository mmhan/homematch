import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Import from our existing modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vector_store.store import PropertyVectorStore


class ConversationState(Enum):
    """Enum for tracking conversation state"""
    GREETING = "greeting"
    PROPERTY_TYPE = "property_type"
    BUDGET = "budget"
    BEDROOMS = "bedrooms"
    BATHROOMS = "bathrooms"
    OUTDOOR_SPACE = "outdoor_space"
    AREAS = "areas"
    COMMUTE = "commute"
    TRANSPORT = "transport"
    AMENITIES = "amenities"
    COMMUNITY = "community"
    FEATURES = "features"
    PRIORITIES = "priorities"
    CONFIRMATION = "confirmation"
    COMPLETE = "complete"


@dataclass
class BuyerPreferences:
    """Data class to store collected buyer preferences"""
    property_type: str = ""
    budget_range: str = ""
    bedrooms: str = ""
    bathrooms: str = ""
    outdoor_space: str = ""
    preferred_areas: str = ""
    commute_location: str = ""
    commute_time: str = ""
    transport_preference: str = ""
    transport_priority: str = ""
    amenities: str = ""
    community_type: str = ""
    must_have_features: str = ""
    deal_breakers: str = ""
    special_requirements: str = ""
    top_priorities: str = ""
    additional_info: str = ""


class PropertyPreferenceCollector:
    """Conversational agent for collecting home buyer preferences"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.preferences = BuyerPreferences()
        self.state = ConversationState.GREETING
        self.conversation_history = []

    def get_greeting_message(self) -> str:
        """Initial greeting message"""
        return """Hello! I'm here to help you find your perfect London property.

I'll ask you a few questions about your preferences to understand what you're looking for. This should take about 2-3 minutes.

Let's start! What type of property are you looking for?

Options include: terraced house, semi-detached house, detached house, flat, studio flat, 1-bed flat, shared ownership, new build apartment, conversion, loft apartment, period house, or something else?"""

    def process_response(self, user_input: str) -> str:
        """Process user response and return next question"""

        # Store the response in conversation history
        self.conversation_history.append(f"User: {user_input}")

        if self.state == ConversationState.GREETING:
            self.preferences.property_type = user_input
            self.state = ConversationState.BUDGET
            response = "Great! What's your budget range?"

        elif self.state == ConversationState.BUDGET:
            self.preferences.budget_range = user_input
            self.state = ConversationState.BEDROOMS
            response = "How many bedrooms do you need? Any flexibility on this?"

        elif self.state == ConversationState.BEDROOMS:
            self.preferences.bedrooms = user_input
            self.state = ConversationState.BATHROOMS
            response = "Any preference on bathrooms? Is an en-suite important?"

        elif self.state == ConversationState.BATHROOMS:
            self.preferences.bathrooms = user_input
            self.state = ConversationState.OUTDOOR_SPACE
            response = "Do you need outdoor space? Garden, balcony, or roof terrace?"

        elif self.state == ConversationState.OUTDOOR_SPACE:
            self.preferences.outdoor_space = user_input
            self.state = ConversationState.AREAS
            response = "Are there specific areas in London you're interested in or want to avoid?"

        elif self.state == ConversationState.AREAS:
            self.preferences.preferred_areas = user_input
            self.state = ConversationState.COMMUTE
            response = "Where do you need to commute to for work? And what's your acceptable commute time?"

        elif self.state == ConversationState.COMMUTE:
            self.preferences.commute_location = user_input
            self.state = ConversationState.TRANSPORT
            response = "Do you prefer tube, bus, rail, or are you flexible with transport? How important are direct transport links?"

        elif self.state == ConversationState.TRANSPORT:
            self.preferences.transport_preference = user_input
            self.state = ConversationState.AMENITIES
            response = "What's important to have nearby: shops, restaurants, parks, gyms, schools? Do you prefer busy areas with nightlife or quieter residential areas?"

        elif self.state == ConversationState.AMENITIES:
            self.preferences.amenities = user_input
            self.state = ConversationState.COMMUNITY
            response = "Do you prefer established family neighborhoods, trendy up-and-coming areas, or central locations?"

        elif self.state == ConversationState.COMMUNITY:
            self.preferences.community_type = user_input
            self.state = ConversationState.FEATURES
            response = "Any must-have features (parking, period features, modern kitchen, etc.) or deal-breakers? Any special requirements?"

        elif self.state == ConversationState.FEATURES:
            self.preferences.must_have_features = user_input
            self.state = ConversationState.PRIORITIES
            response = "If you had to choose, what are your top 3 most important factors from everything we've discussed?"

        elif self.state == ConversationState.PRIORITIES:
            self.preferences.top_priorities = user_input
            self.state = ConversationState.CONFIRMATION
            response = self._generate_summary()

        elif self.state == ConversationState.CONFIRMATION:
            if "yes" in user_input.lower() or "correct" in user_input.lower():
                self.state = ConversationState.COMPLETE
                response = "Perfect! I'll now generate your property search query."
            else:
                self.preferences.additional_info = user_input
                response = "Thanks for the clarification. I'll now generate your property search query."
                self.state = ConversationState.COMPLETE

        else:
            response = "I'm not sure how to respond to that. Could you try again?"

        # Store the response in conversation history
        self.conversation_history.append(f"Assistant: {response}")

        return response

    def _generate_summary(self) -> str:
        """Generate a summary of collected preferences for confirmation"""
        summary = "Let me confirm what I've understood about your preferences:\n\n"

        if self.preferences.property_type:
            summary += f"• Property type: {self.preferences.property_type}\n"
        if self.preferences.budget_range:
            summary += f"• Budget: {self.preferences.budget_range}\n"
        if self.preferences.bedrooms:
            summary += f"• Bedrooms: {self.preferences.bedrooms}\n"
        if self.preferences.bathrooms:
            summary += f"• Bathrooms: {self.preferences.bathrooms}\n"
        if self.preferences.outdoor_space:
            summary += f"• Outdoor space: {self.preferences.outdoor_space}\n"
        if self.preferences.preferred_areas:
            summary += f"• Preferred areas: {self.preferences.preferred_areas}\n"
        if self.preferences.commute_location:
            summary += f"• Commute: {self.preferences.commute_location}\n"
        if self.preferences.transport_preference:
            summary += f"• Transport: {self.preferences.transport_preference}\n"
        if self.preferences.amenities:
            summary += f"• Amenities: {self.preferences.amenities}\n"
        if self.preferences.community_type:
            summary += f"• Community type: {self.preferences.community_type}\n"
        if self.preferences.must_have_features:
            summary += f"• Features: {self.preferences.must_have_features}\n"
        if self.preferences.top_priorities:
            summary += f"• Top priorities: {self.preferences.top_priorities}\n"

        summary += "\nIs this correct? If there's anything else important I should know about your ideal property, please let me know."

        return summary

    def generate_semantic_query(self) -> str:
        """Generate semantic search query from collected preferences"""
        if self.state != ConversationState.COMPLETE:
            raise ValueError("Cannot generate query - preference collection not complete")

        # Create prompt template for query generation
        query_template = PromptTemplate.from_template(
            """Based on the following home buyer preferences, generate a natural language search query
            that would effectively match against London property listings. The query should be detailed
            and include the most important aspects of what the buyer is looking for.

            Buyer Preferences:
            - Property type: {property_type}
            - Budget: {budget_range}
            - Bedrooms: {bedrooms}
            - Bathrooms: {bathrooms}
            - Outdoor space: {outdoor_space}
            - Preferred areas: {preferred_areas}
            - Commute requirements: {commute_location}
            - Transport preferences: {transport_preference}
            - Desired amenities: {amenities}
            - Community type: {community_type}
            - Must-have features: {must_have_features}
            - Top priorities: {top_priorities}
            - Additional info: {additional_info}

            Generate a natural language search query that captures the essence of what this buyer is looking for.
            The query should be optimized for semantic search against property listings.

            Example format: "Modern 2-bedroom flat in Clapham or Islington with good tube links, suitable for young professional, with nearby cafes and nightlife, under £600k"

            Query:"""
        )

        # Generate the query
        chain = query_template | self.llm | StrOutputParser()

        query = chain.invoke({
            "property_type": self.preferences.property_type,
            "budget_range": self.preferences.budget_range,
            "bedrooms": self.preferences.bedrooms,
            "bathrooms": self.preferences.bathrooms,
            "outdoor_space": self.preferences.outdoor_space,
            "preferred_areas": self.preferences.preferred_areas,
            "commute_location": self.preferences.commute_location,
            "transport_preference": self.preferences.transport_preference,
            "amenities": self.preferences.amenities,
            "community_type": self.preferences.community_type,
            "must_have_features": self.preferences.must_have_features,
            "top_priorities": self.preferences.top_priorities,
            "additional_info": self.preferences.additional_info
        })

        return query.strip()

    def is_complete(self) -> bool:
        """Check if preference collection is complete"""
        return self.state == ConversationState.COMPLETE

    def reset(self):
        """Reset the collector for a new conversation"""
        self.preferences = BuyerPreferences()
        self.state = ConversationState.GREETING
        self.conversation_history = []


# Example usage
def main():
    """Example usage of the PropertyPreferenceCollector"""
    collector = PropertyPreferenceCollector()

    print("=== Property Preference Collector Demo ===")
    print(collector.get_greeting_message())

    # Simulate a conversation
    while not collector.is_complete():
        user_input = input("\nYour response: ")
        response = collector.process_response(user_input)
        print(f"\nAssistant: {response}")

    # Generate semantic query
    try:
        semantic_query = collector.generate_semantic_query()
        print(f"\n=== Generated Semantic Search Query ===")
        print(semantic_query)
    except Exception as e:
        print(f"Error generating query: {e}")


if __name__ == "__main__":
    main()


