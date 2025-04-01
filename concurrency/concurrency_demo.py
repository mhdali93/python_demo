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
import aiosqlite
from aiohttp import ClientSession
from sample_employees import sample_employees

# Global constants
DB_FILE = 'simple_demo.db'
SAMPLE_URLS = [
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/1'
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
        CREATE TABLE employee (
            employee_id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            hire_date DATE,
            job_title VARCHAR(50),
            salary DECIMAL(10, 2),
            department VARCHAR(50),
            manager_id INT
        )
    ''')
    
    # Insert sample data
    cursor.executemany('INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_employees)
    
    # Commit and close
    conn.commit()
    conn.close()
    print(f"Database created at {DB_FILE}")

# ===== DATABASE OPERATIONS =====

def sync_db_query(employee_id):
    """Synchronous database query"""
    conn = sqlite3.connect(DB_FILE)
    print(f"Sync Going to Retrieve for {employee_id}")
    time.sleep(0.5)
    cursor = conn.cursor()
    query= """  WITH emp_cte AS (
                        SELECT
                            manager_id,
                            COUNT(1) AS rep,SUM(salary) as tot_rep_sal

                        FROM employee
                        GROUP BY manager_id
                )
                SELECT 
                    e1.*,
                    e2.first_name || ' ' || e2.last_name AS manager_name,
                    CASE 
                        WHEN e3.rep IS NOT NULL THEN e3.rep 
                        ELSE 0 
                        END AS reporters,
                    CASE 
                        WHEN e3.tot_rep_sal IS NOT NULL THEN e3.tot_rep_sal 
                        ELSE 0 
                        END AS team_salary
                    FROM employee e1
                    LEFT JOIN employee e2 ON e2.employee_id = e1.manager_id
                    LEFT JOIN emp_cte e3 ON e3.manager_id = e1.employee_id WHERE e1.employee_id = ?"""
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    return employee

async def async_db_query(employee_id):
    """Asynchronous database query"""
    db = await aiosqlite.connect(DB_FILE)
    await asyncio.sleep(0.5)
    try:
        print(f"Async Going to Retrieve for {employee_id}")
        query= """  WITH emp_cte AS (
                        SELECT
                            manager_id,
                            COUNT(1) AS rep,SUM(salary) as tot_rep_sal

                        FROM employee
                        GROUP BY manager_id
                )
                SELECT 
                    e1.*,
                    e2.first_name || ' ' || e2.last_name AS manager_name,
                    CASE 
                        WHEN e3.rep IS NOT NULL THEN e3.rep 
                        ELSE 0 
                        END AS reporters,
                    CASE 
                        WHEN e3.tot_rep_sal IS NOT NULL THEN e3.tot_rep_sal 
                        ELSE 0 
                        END AS team_salary
                    FROM employee e1
                    LEFT JOIN employee e2 ON e2.employee_id = e1.manager_id
                    LEFT JOIN emp_cte e3 ON e3.manager_id = e1.employee_id WHERE e1.employee_id = ?"""
        async with db.execute(query, (employee_id,)) as cursor:
            row = await cursor.fetchone()
            return row
    finally:
        await db.close()

# ===== THREADING EXAMPLES =====

def download_url(url, thread_name):
    """Function that downloads a URL - I/O bound task"""
    print(f"Thread {thread_name}: Downloading {url}")
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    print(f"Thread {thread_name}: Downloaded {url} in {end_time - start_time:.2f} seconds")
    return response.status_code

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
    
    # Example 3: Database operations no threading
    print("\n--- Example 3: Database Operations (No Threading) ---")
    start_time = time.time()
    for i in range(1, len(sample_employees)+1):
        employee = sync_db_query(i)
        print(f"Retrieved employee {employee[1]}")
    end_time = time.time()
    print(f"Total time without threading: {end_time - start_time:.2f} seconds")

    # Example 4: Database operations with threading
    print("\n--- Example 4: Database Operations (With Threading) ---")
    start_time = time.time()
    db_threads = []
    
    # Create and start threads for database operations
    for i in range(1, len(sample_employees)+1):
        thread = threading.Thread(
            target=lambda x: print(f"Retrieved employee {sync_db_query(x)[1]}"),
            args=(i,)
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
    size = 1500
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
    try:
        async with session.get(url, ssl=False) as response:
            await response.read()
        end_time = time.time()
        print(f"Fetched {url} in {end_time - start_time:.2f} seconds")
        return response.status
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

async def run_async_demo():
    print("\n===== ASYNCIO DEMO =====")
    print("AsyncIO is good for I/O-bound tasks with cooperative multitasking")
    print("Tasks voluntarily yield control when waiting for I/O")
    
    # Example 1: Downloading URLs without asyncio
    print("\n--- Example 1: URL Downloads (No AsyncIO) ---")
    start_time = time.time()
    for i, url in enumerate(SAMPLE_URLS):
        download_url(url, f"Main-{i}")
    end_time = time.time()
    print(f"Total time without asyncio: {end_time - start_time:.2f} seconds")

    # Example 2: Fetching URLs with asyncio
    print("\n--- Example 2: URL Fetches (With AsyncIO) ---")
    start_time = time.time()
    
    # Create a client session
    async with ClientSession() as session:
        # Create tasks for each URL
        tasks = [fetch_url(url, session) for url in SAMPLE_URLS]
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Total time with asyncio: {end_time - start_time:.2f} seconds")
    
    # Example 3: Database operations no asyncio
    print("\n--- Example 3: Database Operations (No AsyncIO) ---")
    start_time = time.time()
    for i in range(1, len(sample_employees)+1):
        employee = sync_db_query(i)
        print(f"Retrieved employee {employee[1]}")
    end_time = time.time()
    print(f"Total time without async: {end_time - start_time:.2f} seconds")

    # Example 4: Database operations with asyncio
    print("\n--- Example 4: Database Operations (With AsyncIO) ---")
    start_time = time.time()
    
    # Create tasks for individual database operations
    db_tasks = [async_db_query(i) for i in range(1, len(sample_employees)+1)]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*db_tasks)
    
    # Print results
    for row in results:
        print(f"Retrieved employee {row[1]}")
    
    end_time = time.time()
    print(f"Total time for async database operations: {end_time - start_time:.2f} seconds")

def main():
    """Main function to run all demos"""
    # Setup database for demos
    setup_database()
    
    # Run threading demo
    # run_threading_demo()
    
    # Run multiprocessing demo
    # run_multiprocessing_demo()
    
    # Run asyncio demo
    asyncio.run(run_async_demo())
    
    print("\n===== CONCURRENCY SUMMARY =====")
    print("1. Threading: Good for I/O-bound tasks, shared memory, limited by GIL")
    print("2. Multiprocessing: Good for CPU-bound tasks, separate memory, bypasses GIL")
    print("3. AsyncIO: Good for I/O-bound tasks, single-threaded, cooperative multitasking")

if __name__ == "__main__":
    main() 