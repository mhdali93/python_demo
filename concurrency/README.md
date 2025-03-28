# Python Concurrency Demo

A simple demo showing three different concurrency models in Python:
- **Threading** - Best for I/O-bound tasks (network, file I/O, database)
- **Multiprocessing** - Best for CPU-bound tasks
- **AsyncIO** - Best for I/O-bound tasks using cooperative multitasking

## Requirements

Install the required packages:

```bash
pip install requests numpy aiohttp
```

## Running the Demo

Simply run the demo script:

```bash
python concurrency_demo.py
```

## What You'll See

The demo will:

1. **Create a simple SQLite database** with sample user data

2. **Run threading examples**:
   - URL downloads (sequential vs. threaded)
   - Database operations with threads

3. **Run multiprocessing examples**:
   - CPU-intensive tasks (sequential vs. parallel)

4. **Run asyncio examples**:
   - URL fetches with async/await
   - Simulated database operations with async/await

5. **Explain the key differences** between the three concurrency models

## Key Takeaways

- **Threading**: Good for I/O-bound tasks, but ineffective for CPU-bound tasks due to the GIL
- **Multiprocessing**: Good for CPU-bound tasks as it bypasses the GIL, but uses more memory
- **AsyncIO**: Good for I/O-bound tasks, uses a single thread with cooperative multitasking

## What is the GIL?

The **Global Interpreter Lock (GIL)** is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode at once. This means:

- **Threads can't run truly in parallel** for CPU-bound tasks
- **Multiprocessing bypasses the GIL** by using separate processes
- **AsyncIO works within a single thread**, so the GIL is not a limitation 