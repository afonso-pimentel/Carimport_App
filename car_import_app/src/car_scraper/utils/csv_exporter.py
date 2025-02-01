import csv

def export_to_csv(cars, filename="best_deals.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Brand", "Model", "Price", "Currency", "Production Date", "Mileage", "Mileage Unit",
                         "Engine Power", "Engine Displacement", "CO2 Emissions", "Fuel Type"])
        for car in cars:
            writer.writerow([car.brand, car.model, car.price, car.currency, car.production_date, car.mileage,
                             car.mileage_unit, car.engine_power, car.engine_displacement, car.co2_emissions, car.fuel_type])
