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
        
    def submit_claim(self, policy_id, amount):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO Claims (PolicyID, ClaimAmount)
                VALUES (?, ?)
            ''', (policy_id, amount))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def update_claim_status(self, claim_id, status):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE Claims SET Status = ? WHERE ClaimID = ?
        ''', (status, claim_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_policy(self, customer_id, policy_type, premium):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Policies (CustomerID, PolicyType, PremiumAmount)
            VALUES (?, ?, ?)
        ''', (customer_id, policy_type, premium))
        self.conn.commit()
        return cursor.lastrowid

    def get_policies(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM Policies WHERE CustomerID = ?
        ''', (customer_id,))
        return cursor.fetchall()

system = InsuranceSystem()
    
cursor.execute(
            "INSERT INTO Branches (BranchName, Location) VALUES (?, ?)",
            ("London", "Twickenham, St Mary's University")
        )
branch_id = cursor.lastrowid
        
cursor.execute(
            "INSERT INTO Customers (Name, Email, BranchID) VALUES (?, ?, ?)",
            ("Justin Roberts", "JustRob@example.com", branch_id)
        )
customer_id = cursor.lastrowid
            
policy_id = system.add_policy(
            customer_id=customer_id,
            policy_type="Auto",
            premium=1000.00,
            start_date="03-05-2025",
            end_date="03-05-2026"
        )
print(f"Added policy ID: {policy_id}")
        
system.submit_claim(
            policy_id=policy_id,
            claim_number="Claim#001",
            amount=2500.00,
            description="Damaged"
        )
         
conn.commit