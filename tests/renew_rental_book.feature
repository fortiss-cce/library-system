Feature: User
    A user that can interact with the library system.

    Background:
        Given I'm an user
        And I know a book
        Given I have borrowed that book

    Scenario: Renewing the rental
        

        When I renew the book rental

        Then I should have the book borrowed
        And I should not get an invoice
        And the book should not be marked as read
        And the rental time should be increased
        And the current fee should be increased
        And the book availability should not change
        And the user should have the correct borrowed book