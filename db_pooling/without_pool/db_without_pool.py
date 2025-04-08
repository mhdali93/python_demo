#!/usr/bin/env python3

"""
Database Operations without Connection Pooling

This script demonstrates database operations where a new connection
is established for each operation. This approach is inefficient for
applications with frequent database access.
"""

import sqlite3
import time
import random
from datetime import datetime

# Configuration
DB_FILE = "example.db"
NUM_OPERATIONS = 10000  # Increased from 100 to 10000 (100x)

def setup_database():
    """Set up the example database with a users table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Drop table if it exists
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

def insert_user(username, email):
    """Insert a single user into the database."""
    # Create a new connection for each insert
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)",
        (username, email, created_at)
    )
    
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    """Retrieve a user by ID."""
    # Create a new connection for each query
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def update_user_email(user_id, new_email):
    """Update a user's email."""
    # Create a new connection for each update
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    
    conn.commit()
    conn.close()

def run_benchmark():
    """Run a benchmark of database operations without connection pooling."""
    print(f"Running benchmark with {NUM_OPERATIONS} operations...")
    
    # Set up fresh database
    setup_database()
    
    # Measure insert operations
    start_time = time.time()
    
    for i in range(1, NUM_OPERATIONS + 1):
        username = f"user{i}"
        email = f"user{i}@example.com"
        insert_user(username, email)
    
    insert_time = time.time() - start_time
    print(f"Insert time: {insert_time:.4f} seconds")
    
    # Measure query operations
    start_time = time.time()
    
    for i in range(1, NUM_OPERATIONS + 1):
        user_id = random.randint(1, NUM_OPERATIONS)
        user = get_user_by_id(user_id)
    
    query_time = time.time() - start_time
    print(f"Query time: {query_time:.4f} seconds")
    
    # Measure update operations
    start_time = time.time()
    
    for i in range(1, NUM_OPERATIONS + 1):
        user_id = random.randint(1, NUM_OPERATIONS)
        new_email = f"updated{user_id}@example.com"
        update_user_email(user_id, new_email)
    
    update_time = time.time() - start_time
    print(f"Update time: {update_time:.4f} seconds")
    
    # Total time
    total_time = insert_time + query_time + update_time
    print(f"Total time: {total_time:.4f} seconds")
    
    return {
        "insert_time": insert_time,
        "query_time": query_time,
        "update_time": update_time,
        "total_time": total_time
    }

if __name__ == "__main__":
    print("Database Operations without Connection Pooling")
    print("=" * 50)
    
    # Run the benchmark
    results = run_benchmark()
    
    print("\nBenchmark Summary:")
    print("-" * 30)
    print(f"Operations: {NUM_OPERATIONS} of each type")
    print(f"Insert time: {results['insert_time']:.4f} seconds")
    print(f"Query time: {results['query_time']:.4f} seconds")
    print(f"Update time: {results['update_time']:.4f} seconds")
    print(f"Total time: {results['total_time']:.4f} seconds") 