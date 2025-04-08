# Database Operations with Connection Pooling

This directory contains examples of database applications that use connection pooling. The examples demonstrate both a custom-built connection pool and SQLAlchemy's built-in connection pooling.

## How Connection Pooling Works

In connection pooling:

1. A pool of database connections is established at startup
2. When an operation needs a connection, it borrows one from the pool
3. When the operation is complete, the connection is returned to the pool
4. Connections are reused for subsequent operations, avoiding the overhead of creating new connections

## Key Files

- `db_with_pool.py`: Example using a custom connection pool implementation
- `sqlalchemy_pool_example.py`: Example using SQLAlchemy's built-in connection pooling (requires SQLAlchemy)

## Benefits of This Approach

1. **Improved Performance**: Reusing connections eliminates the overhead of creating and closing connections for each operation.
2. **Resource Management**: Limits the number of connections to the database, preventing resource exhaustion.
3. **Connection Reuse**: Efficiently reuses connections instead of creating new ones for each operation.
4. **Load Balancing**: Some connection pools can distribute load across multiple database servers.
5. **Transaction Management**: Provides better handling of database transactions.

## Running the Examples

To run the custom pool benchmark:

```bash
python db_with_pool.py
```

To run the SQLAlchemy pool benchmark (requires SQLAlchemy):

```bash
python sqlalchemy_pool_example.py
```

## Results

Each benchmark will measure:

- Time to insert records
- Time to query records
- Time to update records
- Total time for all operations

These results can be compared with the non-pooled example to see the performance improvement.

## Types of Connection Pooling

This directory demonstrates two approaches to connection pooling:

### 1. Custom Connection Pool

The `db_with_pool.py` example implements a simple custom connection pool using a queue. This demonstrates the core concepts of connection pooling without external dependencies.

### 2. SQLAlchemy Connection Pool

The `sqlalchemy_pool_example.py` example uses SQLAlchemy's built-in connection pooling, which provides additional features:

- Connection recycling
- Connection validation
- Timeout handling
- Overflow connections
- Thread safety

## When to Use Connection Pooling

Connection pooling is recommended for:

- Web applications handling multiple concurrent requests
- Applications that need to perform many database operations
- Systems where database connection establishment is a bottleneck
- Environments where database resources are limited and need to be managed efficiently

In most production environments, using an established connection pooling solution like SQLAlchemy is preferred over implementing a custom pool. 