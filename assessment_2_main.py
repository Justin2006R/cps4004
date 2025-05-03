import sqlite3

def initialize_database():
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE,
            PasswordHash TEXT,
            Phone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Policies (
            PolicyID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            PolicyType TEXT CHECK(PolicyType IN ('Health', 'Auto', 'Home')),
            CoverageDetails TEXT,
            PremiumAmount REAL,
            StartDate TEXT,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Claims (
            ClaimID INTEGER PRIMARY KEY AUTOINCREMENT,
            PolicyID INTEGER,
            ClaimAmount REAL,
            IncidentDate TEXT,
            Description TEXT,
            Status TEXT DEFAULT 'Pending' CHECK(Status IN ('Pending', 'Approved', 'Rejected')),
            FOREIGN KEY (PolicyID) REFERENCES Policies(PolicyID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Branches (
            BranchID INTEGER PRIMARY KEY AUTOINCREMENT,
            BranchName TEXT NOT NULL,
            Location TEXT NOT NULL,
            ContactPhone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Adjusters (
            AdjusterID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE,
            BranchID INTEGER,
            FOREIGN KEY (BranchID) REFERENCES Branches(BranchID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ClaimAssignments (
            AssignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClaimID INTEGER NOT NULL,
            AdjusterID INTEGER NOT NULL,
            AssignedDate TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ClaimID) REFERENCES Claims(ClaimID),
            FOREIGN KEY (AdjusterID) REFERENCES Adjusters(AdjusterID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payments (
            PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClaimID INTEGER NOT NULL,
            Amount REAL NOT NULL,
            PaymentDate TEXT DEFAULT CURRENT_TIMESTAMP,
            Method TEXT CHECK(Method IN ('Bank Transfer', 'Check', 'Credit Card')),
            Status TEXT DEFAULT 'Pending' CHECK(Status IN ('Pending', 'Completed', 'Failed')),
            FOREIGN KEY (ClaimID) REFERENCES Claims(ClaimID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ClaimLogs (
            LogID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClaimID INTEGER NOT NULL,
            UserType TEXT CHECK(UserType IN ('Adjuster', 'Customer', 'System')),
            Action TEXT NOT NULL,
            Details TEXT,
            Timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ClaimID) REFERENCES Claims(ClaimID)
        )
    ''')

    conn.commit()
    conn.close()

initialize_database()