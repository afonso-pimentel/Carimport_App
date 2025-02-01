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
                cls.PLATFORM_MAP = json.load(file)  # Load the entire JSON as-is
        except FileNotFoundError:
            print("Error: fuel_types.json not found inside the package.")
            cls.PLATFORM_MAP = {}

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
        
        :param scraped_fuel: The raw scraped fuel type (e.g., "essence")
        :return: The standardized fuel type (e.g., "Petrol")
        """
        if not scraped_fuel:
            return "Unknown"

        scraped_fuel = scraped_fuel.lower()

        # Iterate over the fuel types and check if scraped_fuel exists in their values
        for standard_fuel, platform_values in cls.PLATFORM_MAP.items():
            if scraped_fuel in [value.lower() for value in platform_values.values()]:
                return standard_fuel  # Return the standard fuel type

        return "Unknown"


# Load fuel mappings on import
FuelMapper.load_fuel_map()
