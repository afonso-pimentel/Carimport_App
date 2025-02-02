import json
import importlib.resources

class FuelMapper:
    PLATFORM_MAP = {}
    REVERSE_MAP = {}

    @classmethod
    def load_fuel_map(cls):
        """Loads fuel mappings from the config directory."""
        try:
            with importlib.resources.open_text("car_scraper.config", "fuel_types.json") as file:
                cls.PLATFORM_MAP = json.load(file)
        except FileNotFoundError:
            print("Error: fuel_types.json not found inside the package.")
            cls.PLATFORM_MAP = {}

        try:
            with importlib.resources.open_text("car_scraper.config", "fuel_reverse_mappings.json") as file:
                cls.REVERSE_MAP = json.load(file)
        except FileNotFoundError:
            print("Error: fuel_reverse_mappings.json not found inside the package.")
            cls.REVERSE_MAP = {}

    @classmethod
    def map_fuel(cls, fuel_name, platform):
        """
        Maps a standard fuel type (e.g., "Petrol") to a platform-specific value.

        :param fuel_name: The standard fuel type (e.g., "Petrol", "Diesel", etc.)
        :param platform: The platform name ("autoscout24" or "standvirtual")
        :return: The corresponding platform-specific fuel type
        """
        fuel_entry = cls.PLATFORM_MAP.get(fuel_name)
        return fuel_entry.get(platform, "Unknown") if fuel_entry else "Unknown"
        
    @classmethod
    def get_standard_fuel(cls, scraped_fuel):
        """
        Converts a scraped fuel type into the standard fuel type.

        :param scraped_fuel: The raw scraped fuel type (e.g., "Électrique/Essence")
        :return: The standardized fuel type (e.g., "Hybrid-Petrol")
        """
        if not scraped_fuel:
            return "Unknown"

        scraped_fuel = scraped_fuel.lower()

        for standard_fuel, synonyms in cls.REVERSE_MAP.items():
            if scraped_fuel in [syn.lower() for syn in synonyms]:
                return standard_fuel

        return "Unknown"


# Load fuel mappings on import
FuelMapper.load_fuel_map()
