import json
import os

class Filters:
    """Encapsulates filtering criteria for car searches."""

    def __init__(self, brand="", model="", fuel="", initial_year="", final_year="",
                 initial_km="", final_km="", initial_power="", final_power="",
                 power_type="", price_from="", price_to_autoscout="", price_to_standvirtual=""):
        self.brand = brand
        self.model = model
        self.fuel = fuel
        self.initial_year = initial_year
        self.final_year = final_year
        self.initial_km = initial_km
        self.final_km = final_km
        self.initial_power = initial_power
        self.final_power = final_power
        self.power_type = power_type
        self.price_from = price_from
        self.price_to_autoscout = price_to_autoscout
        self.price_to_standvirtual = price_to_standvirtual

    @classmethod
    def from_json(cls, filepath=None):
        """Loads filters from a JSON file in the config directory."""
        if filepath is None:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "filters.json")

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                return cls(**data)  
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Warning: filters.json not found or corrupted at {filepath}. Using default filters.")
            return cls()

    def to_json(self, filepath=None):
        """Saves filters to a JSON file in the config directory."""
        if filepath is None:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "filters.json")

        with open(filepath, "w") as file:
            json.dump(self.__dict__, file, indent=2)

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
