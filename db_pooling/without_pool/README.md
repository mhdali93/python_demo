# Database Operations without Connection Pooling

This directory contains an example of a database application that does not use connection pooling. Each operation creates a new database connection, uses it, and then closes it immediately.

## How It Works

In this approach:

1. Each database operation (insert, query, update) creates a new connection
2. The connection is closed after the operation is complete
3. No connections are reused

## Key Files

- `db_without_pool.py`: Main example script that demonstrates database operations without connection pooling

## Problems with This Approach

1. **Performance Overhead**: Creating and closing connections is expensive, especially for databases like PostgreSQL or MySQL.
2. **Resource Exhaustion**: Under high load, the system may run out of available connections.
3. **Connection Limit**: Most database servers have a maximum number of concurrent connections.
4. **Latency**: Each operation includes the overhead of establishing a new connection.

## Running the Example

To run the benchmark:

```bash
python db_without_pool.py
```

## Results

The benchmark will measure:

- Time to insert records
- Time to query records
- Time to update records
- Total time for all operations

These results can be compared with the connection pooling example to see the performance difference.

## When This Approach Might Be Acceptable

While connection pooling is generally preferred, there are some cases where a simple connection-per-operation approach might be acceptable:

- Very lightweight applications with minimal database access
- Applications with very low concurrency requirements
- Simple scripts that run infrequently
- Maintenance utilities where performance is not critical

For most production applications, especially web applications or any system with moderate to high database usage, connection pooling is strongly recommended. 