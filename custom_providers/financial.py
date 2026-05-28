"""
Financial and Transaction Custom Providers
"""

from faker import Faker
from faker.providers import BaseProvider
import random
from datetime import datetime, timedelta


class CustomCreditCardProvider(BaseProvider):
    """
    Custom Credit Card Provider with formatting rules and separators.
    Generates credit card numbers for various card types with realistic formatting.
    """

    card_types = {
        'Maestro': {
            'prefix': ['5018', '5020', '5038', '5893', '6304', '6759', '6761', '6762', '6763'],
            'length': 16,
            'pattern': [4, 4, 4, 4]
        },
        'Mastercard': {
            'prefix': ['51', '52', '53', '54', '55'],
            'length': 16,
            'pattern': [4, 4, 4, 4]
        },
        'Visa': {
            'prefix': ['4'],
            'length': 16,
            'pattern': [4, 4, 4, 4]
        },
        'Amex': {
            'prefix': ['34', '37'],
            'length': 15,
            'pattern': [4, 6, 5]
        },
        'Discover': {
            'prefix': ['6011', '622', '64', '65'],
            'length': 16,
            'pattern': [4, 4, 4, 4]
        },
        'Diners': {
            'prefix': ['300', '301', '302', '303', '304', '305', '36', '38'],
            'length': 14,
            'pattern': [4, 6, 4]
        },
        'JCB': {
            'prefix': ['35'],
            'length': 16,
            'pattern': [4, 4, 4, 4]
        }
    }

    separators = [' ', '-', '']

    def credit_card_number(self, card_type=None, with_separator=True, random_spaces=False):
        """Generate a credit card number with optional separators"""
        if not card_type:
            card_type = random.choice(list(self.card_types.keys()))

        card_info = self.card_types[card_type]
        prefix = random.choice(card_info['prefix'])
        length = card_info['length']
        pattern = card_info['pattern']

        # Generate the full number
        number = prefix
        while len(number) < length - 1:
            number += str(random.randint(0, 9))

        # Add Luhn checksum digit
        number += str(self._luhn_checksum(number))

        # Apply formatting
        if with_separator:
            separator = random.choice(self.separators)
            formatted = []
            pos = 0
            for segment_length in pattern:
                formatted.append(number[pos:pos + segment_length])
                pos += segment_length
            result = separator.join(formatted)

            # Randomly add extra spaces for variability
            if random_spaces and random.random() < 0.3:
                result = ' '.join(result.split())

            return result

        return number

    def _luhn_checksum(self, card_number):
        """Calculate Luhn checksum digit"""
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return (10 - (checksum % 10)) % 10

    def card_type(self):
        """Return a random card type"""
        return random.choice(list(self.card_types.keys()))


class CVV(BaseProvider):
    """Generate CVV codes"""

    def cvv(self, length=3):
        """Generate a CVV code (3 or 4 digits)"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])


class ExpiryDateProvider(BaseProvider):
    """Generate credit card expiry dates"""

    def expiry_date(self, future_years=5):
        """Generate a future expiry date in MM/YY format"""
        today = datetime.now()
        months_ahead = random.randint(1, future_years * 12)
        expiry = today + timedelta(days=months_ahead * 30)
        return expiry.strftime("%m/%y")


class CardTypeProvider(BaseProvider):
    """Provide card type names"""

    card_types = ['Credit', 'Debit', 'Prepaid', 'Business', 'Corporate']

    def card_type(self):
        return random.choice(self.card_types)


class BankUSProvider(BaseProvider):
    """US Bank information provider"""

    banks = [
        'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank',
        'U.S. Bank', 'PNC Bank', 'Capital One', 'TD Bank',
        'First Republic Bank', 'HSBC Bank USA'
    ]

    def bank_name(self):
        return random.choice(self.banks)

    def routing_number(self):
        """Generate a 9-digit routing number"""
        return ''.join([str(random.randint(0, 9)) for _ in range(9)])

    def account_number(self):
        """Generate account number (10-12 digits)"""
        length = random.randint(10, 12)
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])


class MoneyProvider(BaseProvider):
    """Generate monetary amounts"""

    def amount(self, min_amount=1, max_amount=10000, decimals=2):
        """Generate a monetary amount"""
        amt = random.uniform(min_amount, max_amount)
        return round(amt, decimals)

    def currency_amount(self, currency='$', min_amount=1, max_amount=10000):
        """Generate formatted currency amount"""
        amt = self.amount(min_amount, max_amount)
        return f"{currency}{amt:.2f}"


class TransactionIDProvider(BaseProvider):
    """Generate transaction IDs"""

    def transaction_id(self, prefix='TXN'):
        """Generate a unique transaction ID"""
        number = random.randint(1000000, 9999999)
        suffix = random.choice(['CC', 'DB', 'ACH', 'WIRE'])
        return f"{prefix}-{number}-{suffix}"


class CreditCardTransactionTypeProvider(BaseProvider):
    """Credit card transaction types"""

    transaction_types = [
        'Purchase', 'Cash Advance', 'Balance Transfer', 'Payment',
        'Fee', 'Interest Charge', 'Credit', 'Refund'
    ]

    def transaction_type(self):
        return random.choice(self.transaction_types)


class CreditCardTransactionDetailProvider(BaseProvider):
    """Generate credit card transaction details"""

    merchants = [
        'AMAZON.COM', 'WALMART', 'TARGET', 'STARBUCKS', 'MCDONALDS',
        'SHELL GAS STATION', 'COSTCO', 'HOME DEPOT', 'BEST BUY',
        'GROCERY STORE', 'RESTAURANT', 'PHARMACY', 'GAS STATION'
    ]

    def transaction_detail(self):
        merchant = random.choice(self.merchants)
        location = random.choice(['NY', 'CA', 'TX', 'FL', 'IL'])
        return f"{merchant} - {location}"


class NonCreditTransactionTypeProvider(BaseProvider):
    """Non-credit transaction types"""

    transaction_types = [
        'Direct Deposit', 'Wire Transfer', 'ACH Transfer', 'Check Deposit',
        'ATM Withdrawal', 'Debit Card Purchase', 'Online Transfer',
        'Mobile Payment', 'Bill Payment'
    ]

    def transaction_type(self):
        return random.choice(self.transaction_types)


class NonCreditTransactionDetailProvider(BaseProvider):
    """Generate non-credit transaction details"""

    def transaction_detail(self):
        details = [
            'Payroll Deposit', 'Rent Payment', 'Utility Bill',
            'Insurance Premium', 'Loan Payment', 'Investment Transfer',
            'P2P Transfer', 'ATM Withdrawal'
        ]
        return random.choice(details)


class DueDateProvider(BaseProvider):
    """Generate due dates"""

    def due_date(self, days_ahead=30):
        """Generate a future due date"""
        today = datetime.now()
        days = random.randint(1, days_ahead)
        due = today + timedelta(days=days)
        return due.strftime("%Y-%m-%d")


class NonCreditCardProvider(BaseProvider):
    """Non-credit card providers (debit, prepaid, etc.)"""

    card_types = ['Debit Card', 'Prepaid Card', 'Gift Card', 'EBT Card']

    def non_credit_card_type(self):
        return random.choice(self.card_types)


class CardOperationProvider(BaseProvider):
    """Card operations"""

    operations = [
        'Activated', 'Deactivated', 'Blocked', 'Unblocked',
        'Reported Lost', 'Reported Stolen', 'Replaced', 'Renewed'
    ]

    def card_operation(self):
        return random.choice(self.operations)


class CardSalutationProvider(BaseProvider):
    """Card-related salutations"""

    salutations = [
        'Thank you for your payment',
        'Your card has been charged',
        'Payment received',
        'Transaction successful',
        'Order confirmed'
    ]

    def card_salutation(self):
        return random.choice(self.salutations)


class CardCustomerSalutationProvider(BaseProvider):
    """Customer salutations for card communications"""

    salutations = [
        'Dear Valued Customer',
        'Dear Cardholder',
        'Hello',
        'Greetings',
        'Dear Member'
    ]

    def customer_salutation(self):
        return random.choice(self.salutations)