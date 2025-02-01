import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from car_scraper.models.car import Car
from car_scraper.models.ad import Ad
from car_scraper.utils.fuel_mapper import FuelMapper

class AutoScout24Scraper:
    BASE_URL = "https://www.autoscout24.fr"

    def __init__(self, filters):
        self.filters = filters  # Expecting an instance of Filters class

    def build_search_url(self, page=1):
        """Constructs the AutoScout24 search URL based on filters."""
        search_params = [
            (self.filters.brand, f"/{self.filters.brand}"),
            (self.filters.model, f"/{self.filters.model}"),
            (self.filters.fuel, f"fuel={self.filters.fuel}&"),
            (self.filters.initial_year, f"fregfrom={self.filters.initial_year}&"),
            (self.filters.final_year, f"fregto={self.filters.final_year}&"),
            (self.filters.initial_km, f"kmfrom={self.filters.initial_km}&"),
            (self.filters.final_km, f"kmto={self.filters.final_km}&"),
            (self.filters.initial_power, f"powerfrom={self.filters.initial_power}&"),
            (self.filters.final_power, f"powerto={self.filters.final_power}&"),
            (self.filters.price_from, f"pricefrom={self.filters.price_from}&"),
            (self.filters.price_to_autoscout, f"priceto={self.filters.price_to_autoscout}&"),
        ]

        url = f"{self.BASE_URL}/lst?atype=C&cy=F&desc=0&"
        url += "&".join(param[1] for param in search_params if param[0])
        url += f"&search_id=random_id&sort=standard&source=listpage_pagination&ustate=N%2CU&page={page}"
        return url

    def fetch_ads(self):
        """Scrapes ads from AutoScout24 and returns a list of Ad objects."""
        ads = []
        page = 1

        while True:
            url = self.build_search_url(page)
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Error fetching {url}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            listings = soup.find_all('a', class_="ListItem_title__ndA4s")

            if not listings:
                break  # No more pages

            for listing in listings:
                ad = self.scrape_car_details(urljoin(self.BASE_URL, listing['href']))
                if ad:
                    ads.append(ad)

            page += 1

        return ads

    def scrape_car_details(self, car_url):
        """Extracts car details from an individual listing."""
        response = requests.get(car_url)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")

        if not script_tag:
            return None

        car_data = json.loads(script_tag.string.strip())
        item = car_data.get("offers", {}).get("itemOffered", {})

        try:
            fuel = soup.find("div", string="Carburant").find_next_sibling("div").get_text(strip=True)
        except AttributeError:
            fuel = "Unknown"

        engine_power = item.get("vehicleEngine", [{}])[0].get("enginePower", [{}])[0].get("value", None)
        engine_displacement = item.get("vehicleEngine", [{}])[0].get("engineDisplacement", {}).get("value", None)
        emissions_co2 = item.get("emissionsCO2", None)

        car = Car(
            brand=item.get("manufacturer", "Unknown"),
            model=item.get("model", "Unknown"),
            price=item.get("offers", {}).get("price", 0),
            currency=item.get("offers", {}).get("priceCurrency", "EUR"),
            production_date=item.get("productionDate", "").split("-")[0],
            mileage=item.get("mileageFromOdometer", {}).get("value", 0),
            mileage_unit=item.get("mileageFromOdometer", {}).get("unitText", "KM"),
            engine_power=engine_power,
            engine_displacement=engine_displacement,
            co2_emissions=emissions_co2,
            fuel_type=FuelMapper.get_standard_fuel(fuel)
        )

        return Ad(source="AutoScout24", url=car_url, car=car)
