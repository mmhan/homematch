"""
Home Buyer Preference Collector Demo
===================================

This demo showcases the PropertyPreferenceCollector with different buyer personas
and includes an interactive mode for testing.
"""

from typing import Dict, List
from personalization.personalize import ListingPersonalizer
from search.search import PropertyPreferenceCollector
from vector_store.store import PropertyVectorStore


class DemoRunner:
    """Runs demo scenarios for different buyer personas"""

    def __init__(self):
        self.collector = PropertyPreferenceCollector()
        self.vector_store = None
        self._setup_vector_store()

    def get_persona_responses(self) -> Dict[str, List[str]]:
        """Get all persona responses in one place"""
        return {
            "Family Areas": [
                "terraced house",  # property type
                "£900,000 to £1,200,000",  # budget
                "3 bedrooms, but 4 would be great",  # bedrooms
                "2 bathrooms, en-suite would be nice",  # bathrooms
                "Yes, we need a garden for the kids",  # outdoor space
                "Richmond or Wimbledon, somewhere family-friendly",  # areas
                "Central London, about 45 minutes is acceptable",  # commute
                "Rail or tube, need reliable transport",  # transport
                "Good schools, parks, family pubs, safe area",  # amenities
                "Established family neighborhoods",  # community
                "Off-street parking, period features would be lovely",  # features
                "Good schools, garden, transport links",  # priorities
                "Yes, that's all correct"  # confirmation
            ],
            "Young Professionals": [
                "modern flat",  # property type
                "£450,000 to £550,000",  # budget
                "1 bedroom, maybe 2 if budget allows",  # bedrooms
                "1 bathroom is fine",  # bathrooms
                "A balcony would be nice but not essential",  # outdoor space
                "Clapham, Islington, or Shoreditch",  # areas
                "Central London, ideally under 30 minutes",  # commute
                "Tube access is essential, Northern or Central line preferred",  # transport
                "Cafes, restaurants, nightlife, gyms nearby",  # amenities
                "Trendy areas with good nightlife",  # community
                "Modern kitchen, good internet, secure building",  # features
                "Transport links, nightlife, modern amenities",  # priorities
                "Yes, sounds perfect"  # confirmation
            ],
            "Luxury Central": [
                "period apartment or penthouse",  # property type
                "£2,500,000 to £3,500,000",  # budget
                "3 bedrooms minimum",  # bedrooms
                "2-3 bathrooms, master en-suite essential",  # bathrooms
                "Private terrace or garden would be perfect",  # outdoor space
                "Kensington, Chelsea, or Mayfair",  # areas
                "Central London, but comfort is more important than time",  # commute
                "Quality transport, but happy to use taxis",  # transport
                "High-end restaurants, boutique shopping, cultural attractions",  # amenities
                "Prestigious central locations",  # community
                "Period features, high-end finishes, concierge service",  # features
                "Location, luxury finishes, period character",  # priorities
                "Yes, exactly what I'm looking for"  # confirmation
            ],
            "Up and Coming Areas": [
                "Victorian conversion or terraced house",  # property type
                "£400,000 to £650,000",  # budget
                "2-3 bedrooms",  # bedrooms
                "1-2 bathrooms",  # bathrooms
                "Small garden or courtyard would be great",  # outdoor space
                "Peckham, Forest Hill, or Walthamstow",  # areas
                "Central London, up to 45 minutes is okay",  # commute
                "Good transport links, Overground or tube",  # transport
                "Local cafes, markets, developing arts scene",  # amenities
                "Up-and-coming areas with potential",  # community
                "Character features, potential for improvement",  # features
                "Good transport, value for money, character",  # priorities
                "Yes, that captures what I want"  # confirmation
            ],
            "First Time Buyer": [
                "studio flat or 1-bed flat",  # property type
                "£250,000 to £350,000",  # budget
                "Studio or 1 bedroom",  # bedrooms
                "1 bathroom is sufficient",  # bathrooms
                "Not essential, but a small balcony would be nice",  # outdoor space
                "Croydon, Woolwich, or outer London zones",  # areas
                "Central London, willing to commute up to an hour",  # commute
                "Regular transport links, doesn't have to be tube",  # transport
                "Basic amenities, shops, maybe a gym nearby",  # amenities
                "Friendly areas, good for first-time buyers",  # community
                "Help to Buy eligible, modern amenities, secure",  # features
                "Affordability, transport links, safe area",  # priorities
                "Yes, perfect for getting on the ladder"  # confirmation
            ],
            "Unique London Properties": [
                "warehouse conversion or loft apartment",  # property type
                "£1,000,000 to £1,500,000",  # budget
                "2-3 bedrooms",  # bedrooms
                "2 bathrooms, modern fittings",  # bathrooms
                "Unique outdoor space, roof terrace maybe",  # outdoor space
                "King's Cross, Canary Wharf, or Bermondsey",  # areas
                "Central London or Canary Wharf",  # commute
                "Good connections, DLR or tube",  # transport
                "Trendy restaurants, cultural attractions, galleries",  # amenities
                "Creative areas with unique character",  # community
                "Industrial character, high ceilings, unique features",  # features
                "Unique character, location, architectural interest",  # priorities
                "Yes, that's exactly the kind of unique property I want"  # confirmation
            ]
        }

    def _setup_vector_store(self):
        """Initialize the vector store for search demonstrations"""
        try:
            self.vector_store = PropertyVectorStore()
            success = self.vector_store.setup_vectorstore()
            if not success:
                print("⚠️  Warning: Vector store setup failed. Search results won't be available.")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize vector store: {e}")

    def run_persona_demo(self, persona_name: str, responses: List[str]) -> None:
        """Run a demo for a specific persona with predefined responses"""
        print(f"\n{'='*60}")
        print(f"🏠 DEMO: {persona_name.upper()} PERSONA")
        print(f"{'='*60}")

        # Reset collector for new demo
        self.collector.reset()

        # Start with greeting
        print("🤖 Assistant:", self.collector.get_greeting_message())
        print()

        # Process each response
        for i, response in enumerate(responses):
            print(f"👤 User: {response}\n")
            assistant_response = self.collector.process_response(response)
            print(f"🤖 Assistant: {assistant_response}\n")

            if self.collector.is_complete():
                break

        # Generate and display semantic query
        if self.collector.is_complete():
            try:
                semantic_query = self.collector.generate_semantic_query()
                print(f"🔍 Generated Semantic Query:")
                print(f"   {semantic_query}")
                print()

                # Perform search if vector store is available
                if self.vector_store:
                    self._demonstrate_search(semantic_query)

            except Exception as e:
                print(f"❌ Error generating query: {e}")
        else:
            print("❌ Demo incomplete - not all preferences collected")

    def _demonstrate_search(self, query: str) -> None:
        """Demonstrate search results using the generated query"""
        try:
            print("🔍 Searching vector database...")
            results = self.vector_store.semantic_search(query, k=1)
            personalizer = ListingPersonalizer()
            personalized_results = personalizer.personalize_listings(results, self.collector.preferences)

            personalizer.display_personalized_results(personalized_results)

        except Exception as e:
            print(f"❌ Search error: {e}")

    def run_all_demos(self):
        """Run all persona demos"""
        persona_responses = self.get_persona_responses()

        for persona_name, responses in persona_responses.items():
            self.run_persona_demo(persona_name, responses)

    def run_interactive_demo(self):
        """Run an interactive demo where user can input their own preferences"""
        print(f"\n{'='*60}")
        print("🎮 INTERACTIVE DEMO")
        print("Now you can input your own preferences!")
        print("(Type 'quit' at any time to exit)")
        print(f"{'='*60}")

        # Reset collector
        self.collector.reset()

        # Start interactive session
        print("🤖 Assistant:", self.collector.get_greeting_message())

        while not self.collector.is_complete():
            try:
                user_input = input("\n👤 Your response: ").strip()

                if user_input.lower() == 'quit':
                    print("👋 Thanks for trying the demo!")
                    return

                if not user_input:
                    print("Please enter a response or type 'quit' to exit.")
                    continue

                response = self.collector.process_response(user_input)
                print(f"🤖 Assistant: {response}")

            except KeyboardInterrupt:
                print("\n👋 Thanks for trying the demo!")
                return
            except Exception as e:
                print(f"❌ Error: {e}")
                break

        # Generate query and search if complete
        if self.collector.is_complete():
            try:
                semantic_query = self.collector.generate_semantic_query()
                print(f"\n🔍 Your Generated Semantic Query:")
                print(f"   {semantic_query}")

                if self.vector_store:
                    print(f"\n🔍 Searching for properties...")
                    self._demonstrate_search(semantic_query)

            except Exception as e:
                print(f"❌ Error generating query: {e}")


def main():
    """Main demo function"""
    print("🏠 Homematch Demo")
    print("=====================================")

    demo = DemoRunner()

    while True:
        print("\nChoose a demo option:")
        print("1. Run all persona demos")
        print("2. Family Areas persona")
        print("3. Young Professionals persona")
        print("4. Luxury Central persona")
        print("5. Up and Coming Areas persona")
        print("6. First Time Buyer persona")
        print("7. Unique London Properties persona")
        print("8. Interactive demo (your own preferences)")
        print("9. Exit")

        try:
            choice = input("\nEnter your choice (1-9): ").strip()

            if choice == '1':
                demo.run_all_demos()
            elif choice in ['2', '3', '4', '5', '6', '7']:
                # Get persona responses once for all individual demos
                persona_responses = demo.get_persona_responses()

                if choice == '2':
                    # Family Areas
                    demo.run_persona_demo("Family Areas", persona_responses["Family Areas"])
                elif choice == '3':
                    # Young Professionals
                    demo.run_persona_demo("Young Professionals", persona_responses["Young Professionals"])
                elif choice == '4':
                    # Luxury Central
                    demo.run_persona_demo("Luxury Central", persona_responses["Luxury Central"])
                elif choice == '5':
                    # Up and Coming
                    demo.run_persona_demo("Up and Coming Areas", persona_responses["Up and Coming Areas"])
                elif choice == '6':
                    # First Time Buyer
                    demo.run_persona_demo("First Time Buyer", persona_responses["First Time Buyer"])
                elif choice == '7':
                    # Unique Properties
                    demo.run_persona_demo("Unique London Properties", persona_responses["Unique London Properties"])
            elif choice == '8':
                demo.run_interactive_demo()
            elif choice == '9':
                print("👋 Thanks for using the demo!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1-9.")

        except KeyboardInterrupt:
            print("\n👋 Thanks for using the demo!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
