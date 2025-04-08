#!/usr/bin/env python3

"""
Simplified Creational Design Patterns Examples
This file contains easy-to-understand examples of creational design patterns:
1. Singleton: One instance of a class
2. Factory: Create objects without specifying exact class
3. Prototype: Copy existing objects
4. Dependency Injection: Pass dependencies from outside

Special Python Features Used:
- __new__: Magic method that controls instance creation (used in Singleton)
- __init__: Magic method for initializing object attributes
- __str__: Magic method that defines string representation of object
- @staticmethod: Decorator to define methods that don't need class instance
- super(): Function to call methods from parent class
"""

import copy

# ===== 1. SINGLETON PATTERN =====
# Ensures only one instance of a class exists

class Logger:
    """
    A simple singleton logger
    
    Special methods:
    - __new__: Controls object creation to ensure only one instance exists
    
    Implementation notes:
    The line 'cls._instance = super().__new__(cls)' is a key part 
    of the singleton pattern. It breaks down as:
    
    1. super() - Gets the parent class of Logger (which is 'object')
    2. .__new__(cls) - Calls the parent's __new__ method to create a new instance
    3. cls._instance = ... - Stores this instance in a class variable for future reuse
    
    This ensures we only create one instance, then return the same instance for
    all future calls.
    """
    _instance = None  # Class-level instance variable
    
    def __new__(cls):
        # If no instance exists, create one
        if cls._instance is None:
            print("Creating a new logger instance")
            cls._instance = super().__new__(cls)
            cls._instance.log_history = []
        return cls._instance
    
    def log(self, message):
        """Add a message to the log"""
        self.log_history.append(message)
        print(f"LOG: {message}")
    
    def get_history(self):
        """Get all logged messages"""
        return self.log_history

def singleton_demo():
    print("\n=== SINGLETON PATTERN ===")
    print("Purpose: Ensure only one instance of a class exists")
    
    # Create first logger
    logger1 = Logger()
    logger1.log("First message")
    
    # Create second logger (actually returns the same instance)
    logger2 = Logger()
    logger2.log("Second message")
    
    # Both loggers are the same object
    print(f"Same object? {logger1 is logger2}")
    print(f"Log history: {logger1.get_history()}")

# ===== 2. FACTORY PATTERN =====
# Creates objects without specifying the exact class

class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    """
    Factory for creating animal objects
    
    Special methods:
    - @staticmethod: Decorator that makes create_animal accessible without an instance
    """
    @staticmethod
    def create_animal(animal_type):
        """
        Factory method to create animals
        
        The @staticmethod decorator allows this method to be called directly from
        the class without creating an instance (AnimalFactory.create_animal())
        """
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

def factory_demo():
    print("\n=== FACTORY PATTERN ===")
    print("Purpose: Create objects without specifying exact class")
    
    # Create a factory
    factory = AnimalFactory()
    
    # Create animals using the factory
    animals = [
        factory.create_animal("dog"),
        factory.create_animal("cat")
    ]
    
    # Make them speak
    for i, animal in enumerate(animals):
        print(f"Animal {i+1} says: {animal.speak()}")

# ===== 3. PROTOTYPE PATTERN =====
# Creates objects by copying existing ones

class Employee:
    """
    Employee class with clone capability
    
    Special methods:
    - __init__: Initializes the object with name, role and info
    - __str__: Provides string representation of the employee
    """
    def __init__(self, name, role):
        """
        Initialize a new Employee
        
        The __init__ magic method is called when a new object is created
        """
        self.name = name
        self.role = role
        self.info = {
            "department": "Engineering",
            "skills": ["Python", "Design Patterns"]
        }
    
    def clone(self):
        """Create a copy of the employee"""
        return copy.deepcopy(self)
    
    def __str__(self):
        """
        String representation of the employee
        
        The __str__ magic method is called when str() is used on the object
        or when the object is printed
        """
        return f"{self.name} ({self.role}) - {self.info}"

def prototype_demo():
    print("\n=== PROTOTYPE PATTERN ===")
    print("Purpose: Create objects by copying existing ones")
    
    # Create original employee
    original = Employee("John", "Developer")
    print(f"Original: {original}")
    
    # Clone the employee
    clone = original.clone()
    clone.name = "Jane"
    clone.role = "Senior Developer"
    clone.info["skills"].append("Leadership")
    print(f"Clone: {clone}")
    
    # Original remains unchanged
    print(f"Original after cloning: {original}")

# ===== 4. DEPENDENCY INJECTION PATTERN =====
# Inject dependencies instead of creating them

class Database:
    """Database interface"""
    def save(self, data):
        pass

class MySQLDatabase(Database):
    """MySQL database implementation"""
    def save(self, data):
        print(f"Saving to MySQL: {data}")

class MongoDBDatabase(Database):
    """MongoDB database implementation"""
    def save(self, data):
        print(f"Saving to MongoDB: {data}")

class UserService:
    """
    User service that needs a database
    
    Special methods:
    - __init__: Used to inject the database dependency
    """
    def __init__(self, database):
        """
        Initialize with an injected database
        
        This constructor receives a database object from outside
        instead of creating one internally. This makes the service:
        1. More flexible (can use any database implementation)
        2. Easier to test (can inject a mock database)
        3. More maintainable (database logic is separate)
        """
        self.database = database
    
    def create_user(self, user_data):
        """Create a new user"""
        # Business logic here
        processed_data = f"Processed: {user_data}"
        self.database.save(processed_data)

class PaymentGateway:
    """Payment gateway interface"""
    def process_payment(self, amount, card_details):
        pass

class StripeGateway(PaymentGateway):
    """Stripe payment gateway implementation"""
    def process_payment(self, amount, card_details):
        print(f"Processing ${amount} payment via Stripe")
        print(f"Card: {card_details['last4']}")
        return {"status": "success", "transaction_id": "stripe_123"}

class PayPalGateway(PaymentGateway):
    """PayPal payment gateway implementation"""
    def process_payment(self, amount, card_details):
        print(f"Processing ${amount} payment via PayPal")
        print(f"Card: {card_details['last4']}")
        return {"status": "success", "transaction_id": "paypal_456"}

class OrderService:
    """
    Order service that needs a payment gateway
    
    Special methods:
    - __init__: Used to inject the payment gateway dependency
    """
    def __init__(self, payment_gateway):
        """
        Initialize with an injected payment gateway
        
        This constructor receives a payment gateway object from outside
        instead of creating one internally. This makes the service:
        1. More flexible (can use any payment gateway)
        2. Easier to test (can inject a mock gateway)
        3. More maintainable (payment logic is separate)
        """
        self.payment_gateway = payment_gateway
    
    def process_order(self, order_data):
        """Process an order with the injected payment gateway"""
        # Business logic here
        amount = order_data['amount']
        card_details = order_data['card_details']
        
        # Use the injected payment gateway
        result = self.payment_gateway.process_payment(amount, card_details)
        
        if result['status'] == 'success':
            print(f"Order processed successfully! Transaction ID: {result['transaction_id']}")
        else:
            print("Payment failed!")

def dependency_injection_demo():
    print("\n=== DEPENDENCY INJECTION PATTERN ===")
    print("Purpose: Pass dependencies from outside")
    
    # Database Example
    print("\n1. Database Example:")
    # Create different database implementations
    mysql_db = MySQLDatabase()
    mongo_db = MongoDBDatabase()
    
    # Create user services with different databases
    mysql_service = UserService(mysql_db)
    mongo_service = UserService(mongo_db)
    
    # Create users (uses injected database)
    mysql_service.create_user({"name": "John", "email": "john@example.com"})
    mongo_service.create_user({"name": "Jane", "email": "jane@example.com"})
    
    # Payment Example
    print("\n2. Payment Example:")
    # Create different payment gateways
    stripe = StripeGateway()
    paypal = PayPalGateway()
    
    # Create order services with different payment gateways
    stripe_service = OrderService(stripe)
    paypal_service = OrderService(paypal)
    
    # Process orders with different payment gateways
    order_data = {
        'amount': 99.99,
        'card_details': {'last4': '4242'}
    }
    
    print("\nProcessing with Stripe:")
    stripe_service.process_order(order_data)
    
    print("\nProcessing with PayPal:")
    paypal_service.process_order(order_data)

def main():
    """Run all demos"""
    # singleton_demo()
    # factory_demo()
    prototype_demo()
    # dependency_injection_demo()

if __name__ == "__main__":
    main() 