# scripts/db.py
"""Shared database utilities for Callie product database"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "products.db"

def get_db() -> sqlite3.Connection:
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_path() -> Path:
    """Get database file path"""
    return DB_PATH