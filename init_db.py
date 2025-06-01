import sqlite3

conn = sqlite3.connect('canteen.db')
cursor = conn.cursor()

# Drop old menu table if it exists
cursor.execute('DROP TABLE IF EXISTS menu')

# Create new menu table with item and price
cursor.execute('''
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    price INTEGER NOT NULL
)
''')

# Drop old parcels table if it exists
cursor.execute('DROP TABLE IF EXISTS parcels')

# Create new parcels table
cursor.execute('''
CREATE TABLE parcels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    item TEXT,
    quantity INTEGER,
    phone TEXT
)
''')

# Insert menu items with prices
cursor.execute("INSERT INTO menu (item, price) VALUES ('Rice thali', 30)")
cursor.execute("INSERT INTO menu (item, price) VALUES ('Chapati bhaji', 25)")
cursor.execute("INSERT INTO menu (item, price) VALUES ('Vada pav', 15)")
cursor.execute("INSERT INTO menu (item, price) VALUES ('Full chai', 7)")
cursor.execute("INSERT INTO menu (item, price) VALUES ('Half chai', 5)")

conn.commit()
conn.close()