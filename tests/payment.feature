Feature: Payment
    An invoice should be payable.

    Background:
        Given there is a user
        And the user has borrowed a book
        And the user returns the book
        And the invoice exists

    Scenario: Receiving an invoice the invoice should be valid
        When I check the invoice

        Then the customer should be correct
        And the items on the invoice should be correct
        And the invoice should not be closed

    Scenario: Paying an invoice with credit card should fail if the card is not valid
        When the user has a non valid credit card
        And the user pays with this card

        Then an exception should be raised
        And the invoice should not be closed
        
    
    Scenario: Paying an invoice with credit card should fail if the cards limit is smaller then the amount to pay
        When the user has a valid credit card
        And the limit of the card is lower than the fee
        And the user pays with this card

        Then the invoice should not be closed
        And the card limit should not change

    Scenario: Paying an invoice with credit card should succeed if all info is correct
        When the user has a valid credit card
        And the limit of the card is higher than the fee
        And the user pays with this card

        Then the invoice should be closed
        And the card limit should be updated
        And the invoice should be updated in storage
   
    Scenario: Paying an invoice with PayPal should fail if the account information is false
        When the user has a non valid PayPal account
        And the user pays with PayPal

        Then an exception should be raised
        And the invoice should not be closed

    Scenario: Paying an invoice with PayPal should succeed if all info is correct
        When the user has a valid PayPal account
        And the user pays with PayPal

        Then the invoice should be closed
        And the account balance should be updated
        And the invoice should be updated in storage
