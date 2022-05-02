# Library System

This is the code for a very simple library system.
The system contains books (``library.model.book``) with their respective authors (``library.model.author``) and publishers (``library.model.publisher``). There are 3 types of books: Paper, Digital and Audio books.
All books can be borrowed by users. Once the users return the books they will receive an invoice (``library.payment.invoice``) for all their returned books.
The user can then pay the invoice either by credit card or using PayPal.

The system does not have any interface, yet. However, there are some tests that may help you understand the use cases / scenarios of the system.

# Your task

The current code is messy. Your task is to refactor the code and create a cleaner and more straight forward structure.
Concentrate on the following classes since they contain mostly all of the logic and refactoring-worthy code:
* ``library.model.book``
* ``library.model.user``
* ``library.payment.invoice``

You are free to change or move existing code, and add new classes and modules. The interfaces and method signatures do not need to stay stable, while the functionality of the code should remain the same.

# Prerequisites

1. Install Python (>= 3.9)
2. Create a virtual environment  
  ```python -m venv .venv```
3. Activate the virtual environment  
  ```source .venv/bin/activate``` (Linux) or ``.venv/Scripts/activate`` (Windows)
4. Install all requirements  
  ```pip install -r requirements.txt```

# Run the system

In order to run the tests activate the environment and run ``pytest --gherkin-terminal-reporter -vv``.