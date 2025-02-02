import requests
import json
from urllib.parse import urlencode
from car_scraper.models.car import Car
from car_scraper.models.ad import Ad
from car_scraper.models.filters import Filters
from car_scraper.utils.fuel_mapper import FuelMapper

class StandvirtualScraper:
    BASE_URL = "https://www.standvirtual.com/api/v1/search/?json=1"

    def __init__(self, filters: Filters):
        self.filters = self.build_filters(filters)

    def build_filters(self, filters: Filters):
        """Maps our standard Filters object to Standvirtual API parameters."""
        return {
            "search[filter_enum_make]": filters.brand.lower(),
            "search[filter_enum_model]": filters.model.lower(),
            "search[filter_enum_fuel_type]": FuelMapper.map_fuel(filters.fuel, "standvirtual"),
            "search[filter_float_engine_power:from]": filters.initial_power,
            "search[filter_float_engine_power:to]": filters.final_power,
            "search[filter_float_first_registration_year:from]": filters.initial_year,
            "search[filter_float_first_registration_year:to]": filters.final_year,
            "search[filter_float_mileage:from]": filters.initial_km,
            "search[filter_float_mileage:to]": filters.final_km,
            "search[filter_float_price:from]": filters.price_from,
            "search[filter_float_price:to]": filters.price_to_standvirtual,
            "search[category]":"29"
        }

    def fetch_ads(self):
        """Fetch ads from Standvirtual API."""
        ads = []
        current_page = 1

        while True:
            # Build API request URL with filters and pagination
            query_string = urlencode({**self.filters, "page": current_page})
            url = f"{self.BASE_URL}&{query_string}"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"Error fetching page {current_page}: {response.text}")
                break

            data = response.json()
            if not data.get("search_result", {}).get("ads"):
                break  # No more ads available

            # Process each ad
            for ad in data["search_result"]["ads"]:
                try:
                    car = self.parse_ad(ad)
                    ads.append(Ad(source="Standvirtual", url=ad["url"], car=car))
                except Exception as e:
                    print(f"Error parsing ad {ad.get('id', 'N/A')}: {e}")

            # Stop if there are no more pages
            if current_page >= data["search_result"].get("total_pages", 1):
                break
            current_page += 1

        return ads

    def parse_ad(self, ad):
        """Extracts car details from the API response."""
        def get_param(key):
            return next((p[1] for p in ad.get("params", []) if p[0] == key), None)

        # Extract fuel type from fuel_type["key"] instead of params
        fuel_raw = ad.get("fuel_type", {}).get("key", "Unknown")

        return Car(
            brand=get_param("Marca") or "Unknown",
            model=get_param("Modelo") or "Unknown",
            price=ad.get("gross_price", "0").replace(" EUR", "").replace(",", "").replace(" ", ""),
            currency="EUR",
            production_date=get_param("Ano"),
            mileage=float(get_param("Quilómetros").replace(" km", "").replace(",", "").replace(" ", "")) if get_param("Quilómetros") else 0,
            mileage_unit="KM",
            engine_power=float(get_param("Potência").replace(" cv", "")) if get_param("Potência") else 0,
            engine_displacement=float(get_param("Cilindrada").replace(" cm3", "").replace(",", "").replace(" ", "")) if get_param("Cilindrada") else 0,
            co2_emissions=float(get_param("Emissões CO2").replace(" g/km", "").replace(",", "").replace(" ", "")) if get_param("Emissões CO2") else 0,
            fuel_type=FuelMapper.get_standard_fuel(fuel_raw)
        )
