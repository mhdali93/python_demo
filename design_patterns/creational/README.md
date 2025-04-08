# Creational Design Patterns

This directory contains examples of creational design patterns in Python. Creational patterns are concerned with the process of object creation.

## Patterns Implemented

### 1. Singleton Pattern
- Ensures only one instance of a class exists
- Useful for:
  - Database connections
  - Configuration managers
  - Logging systems
  - Cache managers

Example: `DatabaseConnection` class that maintains a single connection instance.

### 2. Factory Pattern
- Provides a method to create objects without specifying the exact class
- Useful for:
  - Creating different types of objects based on configuration
  - Abstracting object creation logic
  - Supporting multiple implementations of the same interface

Example: `DocumentFactory` that creates different types of documents (PDF, Word).

### 3. Prototype Pattern
- Creates new objects by copying an existing object
- Useful for:
  - Creating objects that are expensive to create
  - Avoiding building a class hierarchy of factories
  - When classes to instantiate are specified at runtime

Example: `Car` class with cloning capability to create variations of a base car model.

### 4. Dependency Injection Pattern
- Injects dependencies into a class instead of creating them inside the class
- Useful for:
  - Improving testability
  - Making code more flexible and maintainable
  - Following the Dependency Inversion Principle

Example: `UserService` that receives its logger dependency through constructor injection.

Additional Examples:
- Database Service: `UserService` with injected database implementations (MySQL, MongoDB)
- Payment Processing: `OrderService` with injected payment gateways (Stripe, PayPal)

## Running the Examples

To run all the examples:

```bash
python creational_patterns.py
```

Each pattern has its own example function that demonstrates its usage and benefits.

## Key Benefits

1. **Singleton**
   - Ensures single instance
   - Global access point
   - Lazy initialization

2. **Factory**
   - Loose coupling
   - Easy to extend
   - Encapsulates object creation

3. **Prototype**
   - Reduces subclassing
   - Dynamic object creation
   - Efficient object copying

4. **Dependency Injection**
   - Better testability
   - Loose coupling
   - Easier maintenance
   - Flexible implementation switching
   - Clear separation of concerns

## Special Methods Used in Examples

The following special methods (also known as magic methods) are utilized in the examples provided in this directory. Understanding these methods is crucial for grasping how the design patterns work in Python.

1. **`__new__(cls)`**:
   - Used in the Singleton pattern to control the creation of a new instance. It is called before `__init__` and is responsible for returning a new instance of the class.
   - Example in `Logger` class:
     ```python
     def __new__(cls):
         if cls._instance is None:
             cls._instance = super().__new__(cls)
         return cls._instance
     ```

2. **`__init__(self, ...)`**:
   - The constructor method that initializes a new object. It is called when you create a new instance of a class.
   - Used in `UserService` and `OrderService` to inject dependencies.
   - Example:
     ```python
     def __init__(self, database):
         self.database = database
     ```

3. **`__str__(self)`**:
   - Defines the string representation of an object, which is what is returned when you call `str()` on an instance or use `print()`.
   - Used in the `Employee` class to provide a readable string representation.
   - Example:
     ```python
     def __str__(self):
         return f"{self.name} ({self.role}) - {self.info}"
     ```

4. **`@staticmethod`**:
   - A decorator that defines a method that does not require access to the instance or class. It can be called on the class itself.
   - Used in the `AnimalFactory` class to create animals without needing an instance of the factory.
   - Example:
     ```python
     @staticmethod
     def create_animal(animal_type):
         ...
     ```

5. **`super()`**:
   - A built-in function that allows you to call methods from a parent class. It is often used in conjunction with `__init__` and `__new__`.
   - Example in `Logger` class:
     ```python
     cls._instance = super().__new__(cls)
     ```

These special methods enhance the functionality and usability of the classes in the design patterns, making them more intuitive and easier to work with.