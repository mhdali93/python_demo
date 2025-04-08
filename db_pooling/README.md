# Database Connection Pooling

This directory contains examples demonstrating database connection pooling and its benefits compared to systems without pooling.

## What is Database Connection Pooling?

Database connection pooling is a technique used to maintain a cache of database connections that can be reused when future requests to the database are required. Instead of opening and closing connections for each database operation, which is resource-intensive, a pool of reusable connections is maintained.

## Benefits of Connection Pooling

1. **Performance Improvement**: Establishing a database connection is expensive in terms of time and resources. Connection pooling reduces this overhead.
2. **Resource Management**: Limits the number of connections to the database, preventing resource exhaustion.
3. **Connection Reuse**: Enables efficient reuse of connections instead of creating new ones for each operation.
4. **Load Balancing**: Some connection pools can distribute load across multiple database servers.
5. **Transaction Management**: Can provide better handling of database transactions.

## Folder Structure

- **`with_pool/`**: Example demonstrating a system using database connection pooling
  - Shows implementation using popular pooling libraries (SQLAlchemy, psycopg2 pool)
  - Includes performance benchmarks
  
- **`without_pool/`**: Example demonstrating a system without connection pooling
  - Shows the traditional approach of opening and closing connections
  - Includes performance benchmarks for comparison

## Running the Examples

### Quick Start

For the easiest way to run all examples and see a performance comparison:

```bash
# Make the script executable (if needed)
chmod +x run_demo.sh

# Run the demo
./run_demo.sh
```

This script will:
1. Create a virtual environment
2. Install all necessary dependencies
3. Run the performance comparison
4. Generate a visual chart (if matplotlib is installed)

### Manual Approach

Each subfolder contains its own examples and instructions for running them individually:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run individual examples:
```bash
# Run the non-pooled example
python without_pool/db_without_pool.py

# Run the custom pool example
python with_pool/db_with_pool.py

# Run the SQLAlchemy pool example (requires SQLAlchemy)
python with_pool/sqlalchemy_pool_example.py
```

3. Run the comparison:
```bash
python compare_performance.py
```

The examples use SQLite for simplicity, but the concepts apply to any database system.

## When to Use Connection Pooling

- Web applications handling multiple concurrent requests
- Applications that need to perform many database operations
- Systems where database connection establishment is a bottleneck
- Environments where database resources are limited and need to be managed efficiently 