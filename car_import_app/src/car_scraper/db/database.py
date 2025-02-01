import sqlite3

class Database:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT, model TEXT, price REAL, currency TEXT,
            production_date INTEGER, mileage REAL, mileage_unit TEXT,
            engine_power REAL, engine_displacement REAL, co2_emissions REAL, fuel_type TEXT
        )
        """)
        self.conn.commit()

    def save_car(self, car):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO cars (brand, model, price, currency, production_date, mileage, mileage_unit, 
                          engine_power, engine_displacement, co2_emissions, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (car.brand, car.model, car.price, car.currency, car.production_date, car.mileage, 
              car.mileage_unit, car.engine_power, car.engine_displacement, car.co2_emissions, car.fuel_type))
        self.conn.commit()
