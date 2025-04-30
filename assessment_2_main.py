import sqlite3
import hashlib
from datetime import datetime

def main_db():
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL  # admin, adjuster, agent
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS policies (
        policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        policy_number TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,  # auto, home, life
        premium REAL NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS claims (
        claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id INTEGER NOT NULL,
        claim_number TEXT UNIQUE NOT NULL,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT DEFAULT 'submitted',  # submitted, approved, paid, rejected
        FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
    )
    ''')
    
    
