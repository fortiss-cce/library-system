Feature: User
    A user that can interact with the library system.

    Background:
        Given I'm an user
        And I know a book

    Scenario: Returning a book that is borrowed by the user
        Given I have borrowed that book

        When I return the book

        Then I should receive an invoice
        And the invoice should be valid
        And an invoice should be created in the storage
        And the book availability should be updated

    Scenario: Returning a book that is not borrowed by the user
        Given I did not borrow the book

        When I return the book

        Then I should not receive an invoice
        And the book availability should not change