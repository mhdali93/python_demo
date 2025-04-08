#!/usr/bin/env python3

"""
Database Operations with Connection Pooling

This script demonstrates database operations using a connection pool.
Connections are reused, which improves performance for applications
with frequent database access.
"""

import sqlite3
import time
import random
from datetime import datetime
import queue
import threading

# Configuration
DB_FILE = "example.db"
NUM_OPERATIONS = 10000  # Increased from 100 to 10000 (100x)
POOL_SIZE = 20  # Increased from 5 to 20 to handle larger workload

class ConnectionPool:
    """
    A simple database connection pool implementation.
    
    This pool creates and maintains a specified number of database connections
    that can be reused across multiple operations, improving performance.
    """
    
    def __init__(self, db_file, max_connections):
        """Initialize the connection pool."""
        self.db_file = db_file
        self.max_connections = max_connections
        self.pool = queue.Queue(maxsize=max_connections)
        self.size = 0
        self.lock = threading.Lock()
        
        # Pre-populate the pool with connections
        for _ in range(max_connections):
            self._add_connection()
    
    def _add_connection(self):
        """Add a new connection to the pool."""
        conn = sqlite3.connect(self.db_file)
        self.size += 1
        self.pool.put(conn)
    
    def get_connection(self):
        """Get a connection from the pool."""
        # Wait for an available connection
        conn = self.pool.get()
        return conn
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        # If the connection is still valid, put it back in the pool
        if conn:
            self.pool.put(conn)
    
    def close_all(self):
        """Close all connections in the pool."""
        while not self.pool.empty():
            conn = self.pool.get()
            if conn:
                conn.close()
                self.size -= 1

# Create a global connection pool
connection_pool = None

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
    """Insert a single user into the database using a pooled connection."""
    # Get a connection from the pool
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    
    try:
        created_at = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)",
            (username, email, created_at)
        )
        
        conn.commit()
    finally:
        # Return the connection to the pool
        connection_pool.release_connection(conn)

def get_user_by_id(user_id):
    """Retrieve a user by ID using a pooled connection."""
    # Get a connection from the pool
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user
    finally:
        # Return the connection to the pool
        connection_pool.release_connection(conn)

def update_user_email(user_id, new_email):
    """Update a user's email using a pooled connection."""
    # Get a connection from the pool
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE users SET email = ? WHERE id = ?",
            (new_email, user_id)
        )
        
        conn.commit()
    finally:
        # Return the connection to the pool
        connection_pool.release_connection(conn)

def run_benchmark():
    """Run a benchmark of database operations with connection pooling."""
    global connection_pool
    
    print(f"Running benchmark with {NUM_OPERATIONS} operations...")
    print(f"Connection pool size: {POOL_SIZE}")
    
    # Set up fresh database
    setup_database()
    
    # Create connection pool
    connection_pool = ConnectionPool(DB_FILE, POOL_SIZE)
    
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
    
    # Close all connections
    connection_pool.close_all()
    
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
    print("Database Operations with Connection Pooling")
    print("=" * 50)
    
    # Run the benchmark
    results = run_benchmark()
    
    print("\nBenchmark Summary:")
    print("-" * 30)
    print(f"Operations: {NUM_OPERATIONS} of each type")
    print(f"Connection pool size: {POOL_SIZE}")
    print(f"Insert time: {results['insert_time']:.4f} seconds")
    print(f"Query time: {results['query_time']:.4f} seconds")
    print(f"Update time: {results['update_time']:.4f} seconds")
    print(f"Total time: {results['total_time']:.4f} seconds") 