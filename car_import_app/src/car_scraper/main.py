from car_scraper.models.filters import Filters
from car_scraper.scrapers.autoscout24_scraper import AutoScout24Scraper
from car_scraper.scrapers.standvirtual_scraper import StandvirtualScraper
from car_scraper.utils.fuel_mapper import FuelMapper

def add_search_criteria():
    print("Add search criteria:")
    filters = Filters(
        brand=input("Brand: ").strip(),
        model=input("Model: ").strip(),
        fuel=FuelMapper.map_fuel(input("Fuel: ").strip()),
        initial_year=input("Initial year: ").strip(),
        final_year=input("Final year: ").strip(),
        initial_km=input("Initial km: ").strip(),
        final_km=input("Final km: ").strip(),
        initial_power=input("Initial power: ").strip(),
        final_power=input("Final power: ").strip(),
        power_type=input("Power type: ").strip(),
        price_from=input("Price from: ").strip(),
        price_to_autoscout=input("Price to (AutoScout24): ").strip(),
        price_to_standvirtual=input("Price to (StandVirtual): ").strip()
    )

    filters.to_json()
    print("Search criteria saved.")

def scrape_car_info():
    filters = Filters.from_json()
    
    scrapers = [
        AutoScout24Scraper(filters),
        StandvirtualScraper(filters)
    ]

    for scraper in scrapers:
        ads = scraper.fetch_ads()
        print(f"Scraped {len(ads)} ads from {scraper.__class__.__name__}")
        for ad in ads[:5]:  # Print first 5 ads
            print(ad)

def main():
    while True:
        print("\nMenu:")
        print("1. Add search criteria")
        print("2. Scrape car info")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_search_criteria()
        elif choice == '2':
            scrape_car_info()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
