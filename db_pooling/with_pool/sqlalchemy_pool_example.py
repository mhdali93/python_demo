#!/usr/bin/env python3

"""
Database Operations with SQLAlchemy Connection Pooling

This script demonstrates database operations using SQLAlchemy's
built-in connection pooling. This is a more production-ready
approach compared to implementing a custom connection pool.
"""

import time
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

# Configuration
DB_URL = "sqlite:///example_sqlalchemy.db"
NUM_OPERATIONS = 10000  # Increased from 100 to 10000 (100x)
POOL_SIZE = 20  # Increased from 5 to 20
MAX_OVERFLOW = 30  # Increased from 10 to 30

# Create the engine with pooling
engine = create_engine(
    DB_URL,
    poolclass=QueuePool,  # Use QueuePool as the connection pool
    pool_size=POOL_SIZE,  # How many connections to keep open
    max_overflow=MAX_OVERFLOW,  # How many extra connections allowed
    pool_timeout=30,  # Timeout waiting for a connection from the pool
    pool_recycle=1800,  # Recycle connections older than 1800 seconds
)

# Create a base class for declarative models
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

# Create session factory
Session = sessionmaker(bind=engine)

def setup_database():
    """Set up the example database with a users table."""
    # Drop all tables to start fresh
    Base.metadata.drop_all(engine)
    # Create all tables
    Base.metadata.create_all(engine)
    print("Database setup complete.")

def insert_user(username, email):
    """Insert a user into the database using SQLAlchemy's session."""
    # Create a new session from the session factory
    session = Session()
    
    try:
        # Create new user
        user = User(
            username=username,
            email=email,
            created_at=datetime.now().isoformat()
        )
        
        # Add to session and commit
        session.add(user)
        session.commit()
    except Exception as e:
        # Rollback transaction on error
        session.rollback()
        raise e
    finally:
        # Always close the session to return the connection to the pool
        session.close()

def get_user_by_id(user_id):
    """Get a user by ID using SQLAlchemy's session."""
    session = Session()
    
    try:
        # Query for user
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        # Always close the session
        session.close()

def update_user_email(user_id, new_email):
    """Update a user's email using SQLAlchemy's session."""
    session = Session()
    
    try:
        # Get the user
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            # Update email
            user.email = new_email
            session.commit()
    except Exception as e:
        # Rollback transaction on error
        session.rollback()
        raise e
    finally:
        # Always close the session
        session.close()

def run_benchmark():
    """Run a benchmark of database operations with SQLAlchemy's connection pooling."""
    print(f"Running benchmark with {NUM_OPERATIONS} operations...")
    print(f"Connection pool size: {POOL_SIZE} (max overflow: {MAX_OVERFLOW})")
    
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
    
    # Dispose of the engine (close all connections)
    engine.dispose()
    
    # Total time
    total_time = insert_time + query_time + update_time
    print(f"Total time: {total_time:.4f} seconds")
    
    return {
        "insert_time": insert_time,
        "query_time": query_time,
        "update_time": update_time,
        "total_time": total_time
    }

def show_pool_status():
    """Show the current status of the connection pool."""
    status = {
        "size": engine.pool.size(),
        "checkedin": engine.pool.checkedin(),
        "overflow": engine.pool.overflow(),
        "checkedout": engine.pool.checkedout(),
    }
    
    print("\nConnection Pool Status:")
    print(f"Pool Size: {status['size']}")
    print(f"Checked In: {status['checkedin']}")
    print(f"Checked Out: {status['checkedout']}")
    print(f"Overflow: {status['overflow']}")
    
    return status

if __name__ == "__main__":
    print("Database Operations with SQLAlchemy Connection Pooling")
    print("=" * 60)
    
    # Run the benchmark
    results = run_benchmark()
    
    # Show final pool status
    show_pool_status()
    
    print("\nBenchmark Summary:")
    print("-" * 30)
    print(f"Operations: {NUM_OPERATIONS} of each type")
    print(f"Connection pool size: {POOL_SIZE} (max overflow: {MAX_OVERFLOW})")
    print(f"Insert time: {results['insert_time']:.4f} seconds")
    print(f"Query time: {results['query_time']:.4f} seconds")
    print(f"Update time: {results['update_time']:.4f} seconds")
    print(f"Total time: {results['total_time']:.4f} seconds")
    print("\nNote: SQLAlchemy's pooling provides additional features:")
    print("- Connection recycling")
    print("- Dynamic pool resizing (overflow)")
    print("- Automatic validation of connections")
    print("- Connection timeouts") 