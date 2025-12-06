"""
Database module for mobile phone catalog.
Creates and manages SQLite database with mobile phone data.
"""
import sqlite3
from typing import List, Dict, Optional
import json


class PhoneDatabase:
    def __init__(self, db_path: str = None):
        # Use /tmp for serverless environments (Vercel, AWS Lambda, etc.)
        if db_path is None:
            import os
            if os.path.exists("/tmp"):
                # Serverless environment
                self.db_path = "/tmp/phones.db"
            else:
                # Local development
                self.db_path = "phones.db"
        else:
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
                "image_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQ0ej_JOcVolyPNetSu0wPCOGAlapYbe4d8hIUtHHoeOugZZn-1ZxTeWhJLI9_VZZqO_kK2T1Hcmcna1Tw00cp-V1SY_EciOmCZFjdmN7iYjrw9hZM1d5mJWarbhGhDbgQWE4laEr9UgUQ&usqp=CAc"
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
                "image_url": "data:image/jpeg;base64,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W4O4rYStbkS6+pd/dr7m/af3qvS+f6h1LZK6oDTfkaZschGxry/Fh6QCPKvoC1rpy8mxERWUEREBERAREQEREBcnWXQMVfAYJcTeuD43tNnxPGxwXWRExOJzD54zqdVAyGkjYbL0sDj4yRms/e+qPnL90pvwX0BFXpDT5r/qgDUCp+cv3Sm/KvRqFVfOfR2pTfgr8idIPmv+qGNRar5z/dKb8q9Go1X859HalN+CvaKOlT5r/qi/6EVfzn+6U35VBj6lgEhmFXI2V9uUkj5SEyW2Yg12E+ML6QimKRCJ5bTtQfe8f84VP13L33vJPnCp+u/8VfUTrCO9lCPU+l+can67/wAV7730vzjU/Xf+KviKesHeyhHqey/ONT9d/wCKe95J84VP13/ir6ijrB3soPveSfOFT9d/4rGTqcPcCDpCpsf95KPS1wPpX0BFPWDvKv6napwaMicyG5c84pHG+fMLknxkknjkLWBEUqzORERECIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIg//9k="
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
                "image_url": "data:image/webp;base64,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"
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
                "image_url": "data:image/jpeg;base64,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"
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
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKKMkU06o393V0Q515wLSPglqFNNtEjdXFpQ&s"
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
                "image_url": "data:image/jpeg;base64,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"
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
                "image_url": "data:image/jpeg;base64,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"
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
                "image_url": "data:image/jpeg;base64,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"
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
                "image_url": "data:image/jpeg;base64,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"
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

