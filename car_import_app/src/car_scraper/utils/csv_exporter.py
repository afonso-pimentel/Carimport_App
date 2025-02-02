import csv

def export_to_csv(data, cursor, filename="car_ads.csv"):
    """
    Exports car ads stored in the SQLite database to a CSV file.

    :param data: List of car tuples fetched from the database.
    :param cursor: SQLite cursor to retrieve column names.
    :param filename: The filename for the exported CSV.
    """
    if not data:
        print("No data available to export.")
        return

    # Fetch column names from the database schema
    column_names = [desc[0] for desc in cursor.description]

    # Write to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Write header row
        writer.writerows(data)  # Write data rows

    print(f"CSV export successful! File saved as: {filename}")
