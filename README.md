# Library System

This is the code for a very simple library system.
The system contains books with their respective authors and publishers. There are 3 types of books: Paper, Digital and Audio books.
All books can be borrowed by users. Once the users return the books they will receive an invoice for all their returned books. 

The system does not have any interface, yet. However, there are some tests that may help you understand the use cases / scenarios of the system.

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