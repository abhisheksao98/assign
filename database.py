"""
Database module for mobile phone catalog.
Creates and manages SQLite database with mobile phone data.
"""
import sqlite3
from typing import List, Dict, Optional
import json


class PhoneDatabase:
    def __init__(self, db_path: str = "phones.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_database()

    def init_database(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT NOT NULL,
                price INTEGER NOT NULL,
                display_size REAL,
                display_type TEXT,
                processor TEXT,
                ram INTEGER,
                storage INTEGER,
                camera_rear TEXT,
                camera_front TEXT,
                battery INTEGER,
                charging TEXT,
                os TEXT,
                weight REAL,
                dimensions TEXT,
                ois BOOLEAN,
                eis BOOLEAN,
                features TEXT,
                image_url TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def populate_database(self):
        """Populate database with mock mobile phone data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM phones")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        phones = [
            {
                "name": "Pixel 8a",
                "brand": "Google",
                "price": 52999,
                "display_size": 6.1,
                "display_type": "OLED",
                "processor": "Google Tensor G3",
                "ram": 8,
                "storage": 128,
                "camera_rear": "64MP + 13MP",
                "camera_front": "13MP",
                "battery": 4492,
                "charging": "18W wired, 7.5W wireless",
                "os": "Android 14",
                "weight": 188,
                "dimensions": "152.1 x 72.7 x 8.9 mm",
                "ois": True,
                "eis": True,
                "features": "AI features, 7 years updates, IP67",
                "image_url": "https://fdn.gsmarena.com/imgroot/reviews/24/google-pixel-8a/-1024w2/gsmarena_001.jpg"
            },
            {
                "name": "OnePlus 12R",
                "brand": "OnePlus",
                "price": 39999,
                "display_size": 6.78,
                "display_type": "AMOLED",
                "processor": "Snapdragon 8 Gen 2",
                "ram": 8,
                "storage": 128,
                "camera_rear": "50MP + 8MP + 2MP",
                "camera_front": "16MP",
                "battery": 5500,
                "charging": "100W SuperVOOC",
                "os": "OxygenOS 14",
                "weight": 207,
                "dimensions": "163.3 x 75.3 x 8.8 mm",
                "ois": True,
                "eis": True,
                "features": "Fast charging, 120Hz display, Gaming mode",
                "image_url": "https://fdn.gsmarena.com/imgroot/reviews/24/oneplus-12r/-1024w2/gsmarena_001.jpg"
            },
            {
                "name": "Samsung Galaxy S24",
                "brand": "Samsung",
                "price": 79999,
                "display_size": 6.2,
                "display_type": "Dynamic AMOLED",
                "processor": "Exynos 2400",
                "ram": 8,
                "storage": 256,
                "camera_rear": "50MP + 10MP + 12MP",
                "camera_front": "12MP",
                "battery": 4000,
                "charging": "25W wired, 15W wireless",
                "os": "One UI 6.1",
                "weight": 167,
                "dimensions": "147 x 70.6 x 7.6 mm",
                "ois": True,
                "eis": True,
                "features": "AI features, S Pen support, IP68",
                "image_url": "https://images.samsung.com/is/image/samsung/p6pim/in/2401/gallery/in-galaxy-s24-s928-sm-s921bzybins-539916389"
            },
            {
                "name": "Samsung Galaxy A54",
                "brand": "Samsung",
                "price": 38999,
                "display_size": 6.4,
                "display_type": "Super AMOLED",
                "processor": "Exynos 1380",
                "ram": 8,
                "storage": 128,
                "camera_rear": "50MP + 12MP + 5MP",
                "camera_front": "32MP",
                "battery": 5000,
                "charging": "25W",
                "os": "One UI 5.1",
                "weight": 202,
                "dimensions": "158.2 x 76.7 x 8.2 mm",
                "ois": True,
                "eis": True,
                "features": "IP67, 120Hz display",
                "image_url": "https://fdn.gsmarena.com/imgroot/reviews/23/samsung-galaxy-a54-5g/lifestyle/-1024w2/gsmarena_005.jpg"
            },
            {
                "name": "Redmi Note 13 Pro",
                "brand": "Xiaomi",
                "price": 23999,
                "display_size": 6.67,
                "display_type": "AMOLED",
                "processor": "Snapdragon 7s Gen 2",
                "ram": 8,
                "storage": 128,
                "camera_rear": "200MP + 8MP + 2MP",
                "camera_front": "16MP",
                "battery": 5100,
                "charging": "67W Turbo",
                "os": "MIUI 14",
                "weight": 199,
                "dimensions": "161.1 x 74.9 x 8.0 mm",
                "ois": False,
                "eis": True,
                "features": "200MP camera, Fast charging, IP54",
                "image_url": "https://fdn.gsmarena.com/imgroot/reviews/24/xiaomi-redmi-note-13-pro-4g/-1024w2/gsmarena_001.jpg"
            },
            {
                "name": "Nothing Phone 2a",
                "brand": "Nothing",
                "price": 23999,
                "display_size": 6.7,
                "display_type": "AMOLED",
                "processor": "MediaTek Dimensity 7200 Pro",
                "ram": 8,
                "storage": 128,
                "camera_rear": "50MP + 50MP",
                "camera_front": "32MP",
                "battery": 5000,
                "charging": "45W",
                "os": "Nothing OS 2.5",
                "weight": 190,
                "dimensions": "162.1 x 76.4 x 8.6 mm",
                "ois": False,
                "eis": True,
                "features": "Glyph interface, Clean UI",
                "image_url": "https://fdn2.gsmarena.com/vv/pics/nothing/nothing-phone-2a-1.jpg"
            },
            {
                "name": "iPhone 15",
                "brand": "Apple",
                "price": 79900,
                "display_size": 6.1,
                "display_type": "Super Retina XDR",
                "processor": "A16 Bionic",
                "ram": 6,
                "storage": 128,
                "camera_rear": "48MP + 12MP",
                "camera_front": "12MP",
                "battery": 3349,
                "charging": "20W, 15W MagSafe",
                "os": "iOS 17",
                "weight": 171,
                "dimensions": "147.6 x 71.6 x 7.8 mm",
                "ois": True,
                "eis": True,
                "features": "USB-C, Dynamic Island, IP68",
                "image_url": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone-15-finish-select-202309-6-7inch-blue"
            },
            {
                "name": "Vivo V29",
                "brand": "Vivo",
                "price": 33999,
                "display_size": 6.78,
                "display_type": "AMOLED",
                "processor": "Snapdragon 778G",
                "ram": 8,
                "storage": 128,
                "camera_rear": "50MP + 8MP",
                "camera_front": "50MP",
                "battery": 4600,
                "charging": "80W FlashCharge",
                "os": "Funtouch OS 13",
                "weight": 186,
                "dimensions": "164.2 x 74.4 x 7.5 mm",
                "ois": True,
                "eis": True,
                "features": "Aura Light, Portrait mode",
                "image_url": "https://fdn.gsmarena.com/imgroot/reviews/23/vivo-v29/-1024w2/gsmarena_001.jpg"
            },
            {
                "name": "Realme 12 Pro",
                "brand": "Realme",
                "price": 25999,
                "display_size": 6.7,
                "display_type": "AMOLED",
                "processor": "Snapdragon 6 Gen 1",
                "ram": 8,
                "storage": 128,
                "camera_rear": "50MP + 32MP + 2MP",
                "camera_front": "16MP",
                "battery": 5000,
                "charging": "67W SuperVOOC",
                "os": "Realme UI 5.0",
                "weight": 190,
                "dimensions": "161.5 x 74.0 x 8.7 mm",
                "ois": True,
                "eis": True,
                "features": "Premium design, Fast charging",
                "image_url": "https://fdn.gsmarena.com/imgroot/news/24/realme-12-pro-official/-1024w2/gsmarena_000.jpg"
            },
            {
                "name": "Motorola Edge 40",
                "brand": "Motorola",
                "price": 29999,
                "display_size": 6.55,
                "display_type": "pOLED",
                "processor": "MediaTek Dimensity 8020",
                "ram": 8,
                "storage": 256,
                "camera_rear": "50MP + 13MP",
                "camera_front": "32MP",
                "battery": 4400,
                "charging": "68W TurboPower",
                "os": "Near stock Android",
                "weight": 171,
                "dimensions": "158.4 x 71.9 x 7.6 mm",
                "ois": True,
                "eis": True,
                "features": "IP68, Stock Android, Fast charging",
                "image_url": "https://fdn.gsmarena.com/imgroot/reviews/23/motorola-edge-40/-1024w2/gsmarena_001.jpg"
            }
        ]
        
        for phone in phones:
            cursor.execute("""
                INSERT INTO phones (
                    name, brand, price, display_size, display_type, processor,
                    ram, storage, camera_rear, camera_front, battery, charging,
                    os, weight, dimensions, ois, eis, features, image_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                phone["name"], phone["brand"], phone["price"], phone["display_size"],
                phone["display_type"], phone["processor"], phone["ram"], phone["storage"],
                phone["camera_rear"], phone["camera_front"], phone["battery"],
                phone["charging"], phone["os"], phone["weight"], phone["dimensions"],
                phone["ois"], phone["eis"], phone["features"], phone["image_url"]
            ))
        
        conn.commit()
        conn.close()

    def search_phones(self, filters: Dict) -> List[Dict]:
        """Search phones based on filters."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM phones WHERE 1=1"
        params = []
        
        if "max_price" in filters:
            query += " AND price <= ?"
            params.append(filters["max_price"])
        
        if "min_price" in filters:
            query += " AND price >= ?"
            params.append(filters["min_price"])
        
        if "brand" in filters:
            query += " AND LOWER(brand) = LOWER(?)"
            params.append(filters["brand"])
        
        if "min_battery" in filters:
            query += " AND battery >= ?"
            params.append(filters["min_battery"])
        
        if "min_ram" in filters:
            query += " AND ram >= ?"
            params.append(filters["min_ram"])
        
        if "has_ois" in filters:
            query += " AND ois = ?"
            params.append(1 if filters["has_ois"] else 0)
        
        if "max_weight" in filters:
            query += " AND weight <= ?"
            params.append(filters["max_weight"])
        
        if "max_display_size" in filters:
            query += " AND display_size <= ?"
            params.append(filters["max_display_size"])
        
        query += " ORDER BY price ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        phones = [dict(row) for row in rows]
        conn.close()
        
        return phones

    def get_phone_by_name(self, name: str) -> Optional[Dict]:
        """Get a phone by name (fuzzy match)."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM phones WHERE LOWER(name) LIKE ?", (f"%{name.lower()}%",))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None

    def get_phones_by_names(self, names: List[str]) -> List[Dict]:
        """Get multiple phones by names."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        phones = []
        for name in names:
            cursor.execute("SELECT * FROM phones WHERE LOWER(name) LIKE ?", (f"%{name.lower()}%",))
            row = cursor.fetchone()
            if row:
                phones.append(dict(row))
        
        conn.close()
        return phones

    def get_all_phones(self) -> List[Dict]:
        """Get all phones."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM phones ORDER BY price ASC")
        rows = cursor.fetchall()
        phones = [dict(row) for row in rows]
        conn.close()
        
        return phones

