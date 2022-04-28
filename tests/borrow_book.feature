Feature: User
    A user that can interact with the library system.

    Background:
        Given I'm an user

    Scenario: Borrowing a book that is available
        Given I want to to borrow an available book

        When I borrow the book

        Then I should receive a borrowed book
        And the book availability should be updated

    Scenario: Borrowing a book that is unavailable
        Given I want to to borrow an unavailable book

        When I borrow the book
        
        Then I should not receive/borrow book
        And the book availability should not change