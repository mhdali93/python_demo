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
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

# Create the base class for declarative models
Base = declarative_base()

class User(Base):
    """User model for the database"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class SQLAlchemyManager:
    """Manages database operations using SQLAlchemy"""
    
    def __init__(self, db_url="sqlite:///example_sqlalchemy.db", pool_size=20):
        self.engine = create_engine(
            db_url,
            pool_size=pool_size,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
        self.Session = sessionmaker(bind=self.engine)
        self.setup_database()
    
    def setup_database(self):
        """Set up the database and create tables"""
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        print("Database setup complete.")
    
    def insert_user(self, username, email):
        """Insert a user into the database"""
        session = self.Session()
        try:
            user = User(
                username=username,
                email=email,
                created_at=datetime.now()
            )
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            return user
        finally:
            session.close()
    
    def update_user_email(self, user_id, new_email):
        """Update a user's email"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user.email = new_email
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def close(self):
        """Close the engine and dispose of the connection pool"""
        self.engine.dispose()
    
    def show_pool_status(self):
        """Show the current status of the connection pool."""
        status = {
            "size": self.engine.pool.size(),
            "checkedin": self.engine.pool.checkedin(),
            "overflow": self.engine.pool.overflow(),
            "checkedout": self.engine.pool.checkedout(),
        }
        
        print("\nConnection Pool Status:")
        print(f"Pool Size: {status['size']}")
        print(f"Checked In: {status['checkedin']}")
        print(f"Checked Out: {status['checkedout']}")
        print(f"Overflow: {status['overflow']}")
        
        return status

class SQLAlchemyBenchmark:
    """Runs benchmarks on SQLAlchemy database operations"""
    
    def __init__(self, db_manager, num_operations=10000):
        self.db_manager = db_manager
        self.num_operations = num_operations
    
    def run_benchmark(self):
        """Run a benchmark of database operations"""
        print(f"Running benchmark with {self.num_operations} operations...")
        print(f"Connection pool size: {self.db_manager.engine.pool.size()}")
        
        # Measure insert operations
        start_time = time.time()
        
        for i in range(1, self.num_operations + 1):
            username = f"user{i}"
            email = f"user{i}@example.com"
            self.db_manager.insert_user(username, email)
        
        insert_time = time.time() - start_time
        print(f"Insert time: {insert_time:.4f} seconds")
        
        # Measure query operations
        start_time = time.time()
        
        for _ in range(self.num_operations):
            user_id = random.randint(1, self.num_operations)
            self.db_manager.get_user_by_id(user_id)
        
        query_time = time.time() - start_time
        print(f"Query time: {query_time:.4f} seconds")
        
        # Measure update operations
        start_time = time.time()
        
        for _ in range(self.num_operations):
            user_id = random.randint(1, self.num_operations)
            new_email = f"updated{user_id}@example.com"
            self.db_manager.update_user_email(user_id, new_email)
        
        update_time = time.time() - start_time
        print(f"Update time: {update_time:.4f} seconds")
        
        # Show final pool status
        self.db_manager.show_pool_status()
        
        # Close the connection pool
        self.db_manager.close()
        
        # Total time
        total_time = insert_time + query_time + update_time
        print(f"Total time: {total_time:.4f} seconds")
        
        return {
            "insert_time": insert_time,
            "query_time": query_time,
            "update_time": update_time,
            "total_time": total_time
        }

def main():
    """Main function to run the benchmark"""
    print("Database Operations with SQLAlchemy Connection Pooling")
    print("=" * 60)
    
    # Create database manager with SQLAlchemy
    db_manager = SQLAlchemyManager(
        db_url="sqlite:///example_sqlalchemy.db",
        pool_size=20
    )
    
    # Create benchmark instance
    benchmark = SQLAlchemyBenchmark(db_manager, num_operations=10000)
    
    # Run the benchmark
    results = benchmark.run_benchmark()
    
    print("\nBenchmark Summary:")
    print("-" * 30)
    print(f"Operations: {benchmark.num_operations} of each type")
    print(f"Connection pool size: {db_manager.engine.pool.size()}")
    print(f"Insert time: {results['insert_time']:.4f} seconds")
    print(f"Query time: {results['query_time']:.4f} seconds")
    print(f"Update time: {results['update_time']:.4f} seconds")
    print(f"Total time: {results['total_time']:.4f} seconds")
    print("\nNote: SQLAlchemy's pooling provides additional features:")
    print("- Connection recycling")
    print("- Dynamic pool resizing (overflow)")
    print("- Automatic validation of connections")
    print("- Connection timeouts")

if __name__ == "__main__":
    main() 