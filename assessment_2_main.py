import sqlite3

conn = sqlite3.connect('insurance.db')
cursor = conn.cursor()

class InsuranceSystem:
             
    def create_tables(self):    
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Email TEXT UNIQUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Policies (
                PolicyID INTEGER PRIMARY KEY,
                CustomerID INTEGER,
                PolicyType TEXT,
                PremiumAmount REAL,
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Claims (
                ClaimID INTEGER PRIMARY KEY,
                PolicyID INTEGER,
                ClaimAmount REAL,
                Status TEXT DEFAULT 'Pending',
                FOREIGN KEY (PolicyID) REFERENCES Policies(PolicyID)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Branches (
                BranchID INTEGER PRIMARY KEY,
                BranchName TEXT NOT NULL,
                Location TEXT NOT NULL
            )
        ''')

        self.conn.commit()
        
