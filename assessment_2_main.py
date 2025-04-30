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
        role TEXT NOT NULL 
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
        type TEXT NOT NULL,  
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
        status TEXT DEFAULT 'submitted', 
        FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
    )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)")
        
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class InsuranceSystem:
    def __init__(self):
        self.conn = sqlite3.connect('insurance.db')
        main_db()  
    
    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user and user[2] == hash_password(password):
            return {'id': user[0], 'username': user[1], 'role': user[3]}
        return None

    def add_customer(self, name, email=None, phone=None):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", 
                      (name, email, phone))
        self.conn.commit()
        return cursor.lastrowid
    
    def create_policy(self, customer_id, policy_number, policy_type, premium, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO policies 
            (customer_id, policy_number, type, premium, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, policy_number, policy_type, premium, start_date, end_date))
        self.conn.commit()
        return cursor.lastrowid
    
    def submit_claim(self, policy_id, claim_number, description, amount):
        cursor = self.conn.cursor()
        claim_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO claims 
            (policy_id, claim_number, date, description, amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (policy_id, claim_number, claim_date, description, amount))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_claim_status(self, claim_id, new_status):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE claims SET status=? WHERE claim_id=?", (new_status, claim_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_claims_report(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.claim_id, c.claim_number, c.date, c.amount, c.status,
                   p.policy_number, cust.name
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            JOIN customers cust ON p.customer_id = cust.customer_id
            ORDER BY c.date DESC
        ''')
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()