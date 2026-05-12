import sqlite3
import os
from config import config

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_filename = os.path.basename(config.db_name)
        
        self.db_path = os.path.join(base_dir, db_filename)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Read schema.sql from the same directory as this script."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(base_dir, "schema.sql")
        
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                self.cursor.executescript(f.read())
                self.conn.commit()
                print(f"✅ Database initialized at: {self.db_path}")
        else:
            print(f"⚠️ Schema not found at: {schema_path}")

    def add_record(self, table_name: str, user_id: int, data: dict):
        """Universal record addition"""
        data['user_id'] = user_id
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        self.cursor.execute(query, list(data.values()))
        self.conn.commit()

    def get_records(self, table_name: str, user_id: int, filters: dict = None):
        """Universal search by filters"""
        query = f"SELECT * FROM {table_name} WHERE user_id = ?"
        params = [user_id]
        
        if filters:
            for key, value in filters.items():
                query += f" AND {key} LIKE ?"
                params.append(f"%{value}%")
        
        self.cursor.execute(query, tuple(params))
        
        cols = [column[0] for column in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]


# Create a singleton instance
db = Database()