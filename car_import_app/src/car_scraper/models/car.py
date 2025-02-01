class Car:
    def __init__(self, brand, model, price, currency, production_date, mileage, mileage_unit, 
                 engine_power, engine_displacement, co2_emissions, fuel_type):
        self.brand = brand
        self.model = model
        self.price = price
        self.currency = currency
        self.production_date = production_date
        self.mileage = mileage
        self.mileage_unit = mileage_unit
        self.engine_power = engine_power
        self.engine_displacement = engine_displacement
        self.co2_emissions = co2_emissions
        self.fuel_type = fuel_type

    def __str__(self):
        return f"{self.brand} {self.model} ({self.production_date}) - {self.price} {self.currency}"