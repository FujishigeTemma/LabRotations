import logging
import sqlite3


class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def insert(self, table: str, data: dict):
        cursor = self.conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        values = tuple(data.values())
        cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()

    def update_density(self, table: str, id: str, low: float, mid: float, high: float):
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE {table} SET low = ?, mid = ?, high = ? WHERE id = ?", (low, mid, high, id))
        self.conn.commit()

    def list(self, table: str):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logging.error(f"Exception: {exc_type} {exc_value}")
            logging.error(traceback)

        self.close()
