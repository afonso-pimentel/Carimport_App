import sqlite3

class InMemoryDB:
    def __init__(self):
        """Initialize an in-memory SQLite database."""
        self.conn = sqlite3.connect(":memory:")  # In-memory DB
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates a table for storing car ads."""
        self.cursor.execute("""
            CREATE TABLE cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                url TEXT UNIQUE,
                brand TEXT,
                model TEXT,
                price REAL,
                currency TEXT,
                production_date INTEGER,
                mileage REAL,
                mileage_unit TEXT,
                engine_power REAL,
                engine_displacement REAL,
                co2_emissions REAL,
                fuel_type TEXT
            )
        """)
        self.conn.commit()

    def insert_car(self, ad):
        """Inserts a car ad into the database."""
        car = ad.car  # Extract Car object from Ad
        try:
            self.cursor.execute("""
                INSERT INTO cars (source, url, brand, model, price, currency, production_date, mileage, 
                                  mileage_unit, engine_power, engine_displacement, co2_emissions, fuel_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ad.source, ad.url, car.brand, car.model, car.price, car.currency, car.production_date, 
                  car.mileage, car.mileage_unit, car.engine_power, car.engine_displacement, car.co2_emissions, car.fuel_type))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Duplicate entry skipped: {ad.url}")

    def fetch_all_cars(self):
        """Fetch all stored car ads."""
        self.cursor.execute("SELECT * FROM cars")
        return self.cursor.fetchall()

    def compare_cars(self):
        """Example: Compare cars across sources."""
        self.cursor.execute("""
            SELECT brand, model, price, source FROM cars 
            ORDER BY brand, model, price ASC
        """)
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
