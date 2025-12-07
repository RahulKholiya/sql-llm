# setup_animals_db.py

import sqlite3
import os

DB_PATH = "data/animals.db"

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Delete the old database file if it exists, to start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# --- Create Habitats Table ---
# This table will store information about where animals live.
table_habitats = """
CREATE TABLE Habitats (
    HabitatID INTEGER PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Continent VARCHAR(50),
    Climate VARCHAR(50)
);
"""
cursor.execute(table_habitats)

# --- Create Animals Table ---
# This table will store information about the animals.
# It uses a 'FOREIGN KEY' to link to the Habitats table.
table_animals = """
CREATE TABLE Animals (
    AnimalID INTEGER PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Classification VARCHAR(50), -- e.g., Mammal, Bird, Reptile
    AverageLifespan INTEGER,
    Diet VARCHAR(20), -- e.g., Carnivore, Herbivore, Omnivore
    HabitatID INTEGER,
    FOREIGN KEY (HabitatID) REFERENCES Habitats(HabitatID)
);
"""
cursor.execute(table_animals)

# --- Insert Data into Habitats ---
habitats_data = [
    (1, 'African Savanna', 'Africa', 'Tropical'),
    (2, 'Amazon Rainforest', 'South America', 'Tropical'),
    (3, 'Arctic Tundra', 'Arctic', 'Polar'),
    (4, 'Antarctica', 'Antarctica', 'Polar'),
    (5, 'Great Barrier Reef', 'Australia', 'Tropical')
]
cursor.executemany("INSERT INTO Habitats VALUES (?, ?, ?, ?)", habitats_data)

# --- Insert Data into Animals ---
animals_data = [
    (1, 'Lion', 'Mammal', 12, 'Carnivore', 1),
    (2, 'African Elephant', 'Mammal', 70, 'Herbivore', 1),
    (3, 'Zebra', 'Mammal', 25, 'Herbivore', 1),
    (4, 'Macaw', 'Bird', 50, 'Herbivore', 2),
    (5, 'Jaguar', 'Mammal', 15, 'Carnivore', 2),
    (6, 'Poison Dart Frog', 'Amphibian', 10, 'Carnivore', 2),
    (7, 'Polar Bear', 'Mammal', 25, 'Carnivore', 3),
    (8, 'Arctic Fox', 'Mammal', 5, 'Omnivore', 3),
    (9, 'Emperor Penguin', 'Bird', 20, 'Carnivore', 4),
    (10, 'Clownfish', 'Fish', 8, 'Omnivore', 5),
    (11, 'Sea Turtle', 'Reptile', 80, 'Omnivore', 5)
]
cursor.executemany("INSERT INTO Animals VALUES (?, ?, ?, ?, ?, ?)", animals_data)

# Commit changes and close the connection
connection.commit()
connection.close()

print(f"Database '{DB_PATH}' created successfully with Animals and Habitats tables.")
print("You can now upload 'data/animals.db' to the Streamlit app.")