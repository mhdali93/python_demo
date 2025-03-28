#!/usr/bin/env python3

"""
Python Concurrency Demo
A simple guide to threading, multiprocessing, and asyncio with basic examples
"""

import os
import time
import threading
import multiprocessing
import asyncio
import requests
import sqlite3
import numpy as np

# Global constants
DB_FILE = 'simple_demo.db'
SAMPLE_URLS = [
    'https://httpbin.org/delay/1',
    'https://httpbin.org/delay/1',
    'https://httpbin.org/delay/1',
    'https://httpbin.org/delay/1'
]

def setup_database():
    """Create a simple SQLite database for our demos"""
    # Remove the database if it already exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Create a new database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create a simple table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    
    # Insert sample data
    sample_users = [
        (1, 'Alice', 'alice@example.com'),
        (2, 'Bob', 'bob@example.com'),
        (3, 'Charlie', 'charlie@example.com'),
        (4, 'Dave', 'dave@example.com'),
        (5, 'Eve', 'eve@example.com')
    ]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?)', sample_users)
    
    # Commit and close
    conn.commit()
    conn.close()
    print(f"Database created at {DB_FILE}")

# ===== THREADING EXAMPLES =====

def download_url(url, thread_name):
    """Function that downloads a URL - I/O bound task"""
    print(f"Thread {thread_name}: Downloading {url}")
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    print(f"Thread {thread_name}: Downloaded {url} in {end_time - start_time:.2f} seconds")
    return response.status_code

def database_operation(user_id, thread_name):
    """Function that performs a database read - I/O bound task"""
    print(f"Thread {thread_name}: Getting user {user_id}")
    
    # Connect to database (each thread needs its own connection)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Simulate a slower database query with a sleep
    time.sleep(1)
    
    # Query the database
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    # Close connection
    conn.close()
    
    print(f"Thread {thread_name}: Retrieved user {user[1]}")
    return user

def run_threading_demo():
    print("\n===== THREADING DEMO =====")
    print("Threading is good for I/O-bound tasks (network, file I/O, database)")
    print("Threads share memory space but can't run in parallel for CPU tasks due to GIL")
    
    # Example 1: Downloading URLs without threading
    print("\n--- Example 1: URL Downloads (No Threading) ---")
    start_time = time.time()
    for i, url in enumerate(SAMPLE_URLS):
        download_url(url, f"Main-{i}")
    end_time = time.time()
    print(f"Total time without threading: {end_time - start_time:.2f} seconds")
    
    # Example 2: Downloading URLs with threading
    print("\n--- Example 2: URL Downloads (With Threading) ---")
    start_time = time.time()
    threads = []
    
    # Create and start threads
    for i, url in enumerate(SAMPLE_URLS):
        thread = threading.Thread(
            target=download_url, 
            args=(url, f"Worker-{i}")
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Total time with threading: {end_time - start_time:.2f} seconds")
    
    # Example 3: Database operations with threading
    print("\n--- Example 3: Database Operations (With Threading) ---")
    start_time = time.time()
    db_threads = []
    
    # Create and start threads for database operations
    for i in range(1, 6):
        thread = threading.Thread(
            target=database_operation, 
            args=(i, f"DB-Worker-{i}")
        )
        db_threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in db_threads:
        thread.join()
    
    end_time = time.time()
    print(f"Total time for database operations: {end_time - start_time:.2f} seconds")

# ===== MULTIPROCESSING EXAMPLES =====

def cpu_intensive_task(n):
    """A CPU-intensive task (matrix multiplication) - CPU bound task"""
    print(f"Process {os.getpid()}: Starting matrix multiplication")
    start_time = time.time()
    
    # Create two random matrices
    size = 500
    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)
    
    # Perform matrix multiplication n times
    for _ in range(n):
        result = np.matmul(matrix_a, matrix_b)
    
    end_time = time.time()
    print(f"Process {os.getpid()}: Completed in {end_time - start_time:.2f} seconds")
    return np.sum(result)

def run_multiprocessing_demo():
    print("\n===== MULTIPROCESSING DEMO =====")
    print("Multiprocessing is good for CPU-bound tasks that need to bypass the GIL")
    print("Each process has its own memory space - higher memory usage")
    
    # Example 1: CPU-intensive task without multiprocessing
    print("\n--- Example 1: CPU-Intensive Task (No Multiprocessing) ---")
    start_time = time.time()
    for i in range(4):
        cpu_intensive_task(1)
    end_time = time.time()
    print(f"Total time without multiprocessing: {end_time - start_time:.2f} seconds")
    
    # Example 2: CPU-intensive task with multiprocessing
    print("\n--- Example 2: CPU-Intensive Task (With Multiprocessing) ---")
    start_time = time.time()
    
    # Create a pool of worker processes (default is number of CPU cores)
    with multiprocessing.Pool() as pool:
        # Run the same task on multiple processes
        results = pool.map(cpu_intensive_task, [1, 1, 1, 1])
    
    end_time = time.time()
    print(f"Total time with multiprocessing: {end_time - start_time:.2f} seconds")

# ===== ASYNCIO EXAMPLES =====

async def fetch_url(url, session):
    """Async function to fetch a URL - I/O bound task"""
    print(f"Fetching {url}")
    start_time = time.time()
    async with session.get(url) as response:
        await response.read()
    end_time = time.time()
    print(f"Fetched {url} in {end_time - start_time:.2f} seconds")
    return response.status

async def async_database_operation(user_id):
    """Simulate an async database operation"""
    print(f"Getting user {user_id}")
    # Simulate I/O operation with sleep
    await asyncio.sleep(1)
    print(f"Retrieved user {user_id}")
    return user_id

async def run_async_demo():
    print("\n===== ASYNCIO DEMO =====")
    print("AsyncIO is good for I/O-bound tasks with cooperative multitasking")
    print("Tasks voluntarily yield control when waiting for I/O")
    
    # Example 1: Fetching URLs with asyncio
    print("\n--- Example 1: URL Fetches (With AsyncIO) ---")
    import aiohttp
    
    start_time = time.time()
    
    # Create a client session
    async with aiohttp.ClientSession() as session:
        # Create tasks for each URL
        tasks = [fetch_url(url, session) for url in SAMPLE_URLS]
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Total time with asyncio: {end_time - start_time:.2f} seconds")
    
    # Example 2: Simulated database operations with asyncio
    print("\n--- Example 2: Simulated Database Operations (With AsyncIO) ---")
    start_time = time.time()
    
    # Create tasks for database operations
    db_tasks = [async_database_operation(i) for i in range(1, 6)]
    
    # Wait for all tasks to complete
    await asyncio.gather(*db_tasks)
    
    end_time = time.time()
    print(f"Total time for async database operations: {end_time - start_time:.2f} seconds")

def main():
    """Main function to run all demos"""
    # Setup database for demos
    setup_database()
    
    # Run threading demo
    run_threading_demo()
    
    # Run multiprocessing demo
    run_multiprocessing_demo()
    
    # Run asyncio demo
    asyncio.run(run_async_demo())
    
    print("\n===== CONCURRENCY SUMMARY =====")
    print("1. Threading: Good for I/O-bound tasks, shared memory, limited by GIL")
    print("2. Multiprocessing: Good for CPU-bound tasks, separate memory, bypasses GIL")
    print("3. AsyncIO: Good for I/O-bound tasks, single-threaded, cooperative multitasking")

if __name__ == "__main__":
    main() 