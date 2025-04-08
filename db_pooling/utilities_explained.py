#!/usr/bin/env python3

"""
System Libraries Explained

This file demonstrates and explains the system libraries 
used in the database connection pooling examples.
"""

import sys
import os
import subprocess
import time
import random
import queue
import threading

class SystemModule:
    """Demonstrates sys module functionality"""
    
    @staticmethod
    def show_info():
        print("\n1. sys Module")
        print("The sys module provides access to variables and functions specific to the Python interpreter.")
        print("Common uses:")
        
        # Show Python version
        print(f"- Python Version: {sys.version}")
        
        # Show command line arguments
        print(f"- Command Line Arguments: {sys.argv}")
        
        # Show module search path
        print(f"- Module Search Path: First 2 paths: {sys.path[:2]}")
        print(f"- Module Search Path: {sys.path}")
        
        # Show platform
        print(f"- Platform: {sys.platform}")

class OSModule:
    """Demonstrates os module functionality"""
    
    @staticmethod
    def show_info():
        print("\n2. os Module")
        print("The os module provides functions for interacting with the operating system.")
        print("Common uses:")
        
        # Current working directory
        print(f"- Current Working Directory: {os.getcwd()}")
        print(f"- Current Dir: {os.curdir}")
        print(f"- Current Dir Path: {os.path.join(os.curdir, 'with_pool', 'README.md')}")
        print(f"- LS dir: {os.listdir()}")
        
        # Environment variables
        print(f"- Sample Environment Variable (PATH): {os.environ.get('PATH', 'Not set')}")
        
        # List files in current directory
        print(f"- Files in Current Directory: \n{os.listdir('.')}")
        
        # Join paths in OS-specific way
        print(f"- Path Joining Example: {os.path.join('folder', 'subfolder', 'file.txt')}")
        
        # Check if file exists
        print(f"- Does this file exist? {os.path.exists(__file__)}")
        print(f"- Does this file exist? {os.path.exists(os.path.join('folder', 'subfolder', 'file.txt'))}")
        print(f"- Does this file exist? {os.path.exists(os.path.join(os.curdir, 'with_pool', 'README.md'))}")

class SubprocessModule:
    """Demonstrates subprocess module functionality"""
    
    @staticmethod
    def show_info():
        print("\n3. subprocess Module")
        print("The subprocess module allows you to spawn new processes and communicate with them.")
        print("Common uses:")
        
        # Run a simple command and capture output
        result = subprocess.run(["echo", "Hello from subprocess"], capture_output=True, text=True)
        print(f"- Run a command: echo 'Hello from subprocess'")
        print(f"  Output: {result.stdout.strip()}")
        print(f"  Return Code: {result.returncode}")

class TimeModule:
    """Demonstrates time module functionality"""
    
    @staticmethod
    def show_info():
        print("\n4. time Module")
        print("The time module provides functions for working with time.")
        print("Common uses:")
        
        # Current time
        print(f"- Current Time (seconds since epoch): {time.time()}")
        
        # Formatted time
        print(f"- Formatted Current Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Sleep example
        print("- Sleep Example (pausing for 1 second)...")
        time.sleep(1)
        print("  ...done!")

class RandomModule:
    """Demonstrates random module functionality"""
    
    @staticmethod
    def show_info():
        print("\n5. random Module")
        print("The random module is used for generating pseudo-random numbers.")
        print("Common uses:")
        
        # Random integer
        print(f"- Random Integer (1-100): {random.randint(1, 100)}")
        
        # Random choice from sequence
        colors = ["red", "green", "blue", "yellow"]
        print(f"- Random Choice from {colors}: {random.choice(colors)}")
        
        # Shuffle a list
        numbers = [1, 2, 3, 4, 5]
        random.shuffle(numbers)
        print(f"- Shuffled List [1,2,3,4,5]: {numbers}")

class QueueModule:
    """Demonstrates queue module functionality"""
    
    @staticmethod
    def show_info():
        print("\n6. queue Module")
        print("The queue module provides a thread-safe FIFO implementation.")
        print("Common uses in connection pooling:")
        
        # Create a queue
        q = queue.Queue(maxsize=3)
        print(f"- Created Queue with maxsize=3")
        print(f"- Queue Empty: {q.empty()}")
        
        # Put items in the queue
        for i in range(3):
            q.put(f"Connection {i}")
            print(f"  Added Connection {i} to Queue")
        
        print(f"- Queue Full: {q.full()}")
        
        # Get items from the queue
        print("- Getting items from the queue:")
        while not q.empty():
            print(f"  Got: {q.get()}")
            print(f"  Got: {q.qsize()}")

class ThreadingModule:
    """Demonstrates threading module functionality"""
    
    @staticmethod
    def worker(name):
        print(f"  Thread {name} starting work")
        time.sleep(1)  # Simulate some work
        print(f"  Thread {name} finished work")
    
    @classmethod
    def show_info(cls):
        print("\n7. threading Module")
        print("The threading module allows concurrent execution.")
        print("Common uses in connection pooling:")
        
        # Create and start threads
        print("- Creating and starting threads:")
        threads = []
        for i in range(3):
            t = threading.Thread(target=cls.worker, args=(f"Worker-{i}",))
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        print("- All threads completed")

class ConnectionPoolingExample:
    """Shows how these libraries are used in connection pooling"""
    
    @staticmethod
    def show_info():
        print("\n=== How These Libraries Are Used in Database Connection Pooling ===")
        print("""
            1. sys: Used to access command-line arguments and interpreter information
               - In compare_performance.py, sys.executable gets the Python interpreter path

            2. os: Used for file and path operations
               - Checking/creating database files
               - Determining script directories
               - Environment variable checking

            3. subprocess: Used to run external Python scripts
               - In compare_performance.py to run each benchmark script separately

            4. time: Used for timing operations and benchmarking
               - Measuring how long database operations take
               - Calculating performance improvements

            5. random: Used to generate test data
               - Creating random user IDs for testing
               - Selecting random records to update

            6. queue: Core of the connection pool implementation
               - Storing database connections
               - Thread-safe borrowing and returning of connections

            7. threading: Used for thread safety in connection pooling
               - Ensuring thread-safe access to the connection pool
               - Locking mechanisms for shared resources

            This combination of libraries enables the creation of an efficient connection
            pooling system that can significantly improve database performance.
            """
         )

def main():
    """Main function to demonstrate all modules"""
    print("=== System Libraries Explained ===")
    print("This file demonstrates common system libraries used in Python applications.\n")
    
    # Show information from each module
    SystemModule.show_info()
    OSModule.show_info()
    SubprocessModule.show_info()
    TimeModule.show_info()
    RandomModule.show_info()
    QueueModule.show_info()
    ThreadingModule.show_info()
    ConnectionPoolingExample.show_info()

if __name__ == "__main__":
    main()
    print("\nYou can run this file directly to see examples of each library in action.")
    print("python utilities_explained.py") 