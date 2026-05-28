"""
Identification and Documentation Custom Providers
"""

from faker.providers import BaseProvider
import random
import string
from datetime import datetime, timedelta


class CustomSSNUSProvider(BaseProvider):
    """Generate US Social Security Numbers"""

    def ssn(self, with_separator=True):
        """Generate a US SSN in format XXX-XX-XXXX"""
        # Area number (001-899, excluding 666)
        area = random.randint(1, 899)
        while area == 666:
            area = random.randint(1, 899)

        # Group number (01-99)
        group = random.randint(1, 99)

        # Serial number (0001-9999)
        serial = random.randint(1, 9999)

        if with_separator:
            return f"{area:03d}-{group:02d}-{serial:04d}"
        return f"{area:03d}{group:02d}{serial:04d}"


class UsDriverLicenseProvider(BaseProvider):
    """Generate US Driver's License numbers"""

    # Different states have different formats
    state_formats = {
        'CA': 'A1234567',    # 1 letter + 7 digits
        'NY': 'A1234567890123456',  # 1 letter + 7-18 digits
        'TX': '12345678',    # 7-8 digits
        'FL': 'A123-456-78-901-0',  # Letter + 12 digits with dashes
        'IL': 'A123-4567-8901',     # Letter + 11 digits with dashes
        'PA': '12345678',    # 8 digits
        'OH': 'AA123456',    # 2 letters + 6 digits
        'GA': '123456789',   # 7-9 digits
        'NC': '12345678901', # 1-12 digits
        'MI': 'A123456789012'  # Letter + 12 digits
    }

    def driver_license(self, state=None):
        """Generate a driver's license number"""
        if not state:
            state = random.choice(list(self.state_formats.keys()))

        format_pattern = self.state_formats.get(state, 'A1234567890')

        result = ''
        for char in format_pattern:
            if char == 'A':
                result += random.choice(string.ascii_uppercase)
            elif char.isdigit():
                result += str(random.randint(0, 9))
            else:
                result += char

        return result, state


class PassportProvider(BaseProvider):
    """Generate passport numbers"""

    def passport_number(self, country='US'):
        """Generate a passport number"""
        if country == 'US':
            # US passport: 9 digits
            return ''.join([str(random.randint(0, 9)) for _ in range(9)])
        elif country == 'UK':
            # UK passport: 9 digits
            return ''.join([str(random.randint(0, 9)) for _ in range(9)])
        else:
            # Generic: 2 letters + 7 digits
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            return letters + numbers

    def passport_expiry(self, years_valid=10):
        """Generate passport expiry date"""
        today = datetime.now()
        expiry = today + timedelta(days=365 * years_valid)
        return expiry.strftime("%Y-%m-%d")


class DocumentIDProvider(BaseProvider):
    """Generate generic document IDs"""

    def document_id(self, prefix='DOC'):
        """Generate a document ID"""
        number = random.randint(100000, 999999)
        year = datetime.now().year
        return f"{prefix}-{year}-{number}"


class RegionIDProvider(BaseProvider):
    """Generate region/state IDs"""

    us_states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'
    }

    def state_code(self):
        """Return a random US state code"""
        return random.choice(list(self.us_states.keys()))

    def state_name(self):
        """Return a random US state name"""
        return random.choice(list(self.us_states.values()))

    def region_id(self):
        """Generate a region ID"""
        state = self.state_code()
        number = random.randint(1000, 9999)
        return f"{state}-{number}"


class UserIDProvider(BaseProvider):
    """Generate user IDs"""

    def user_id(self, prefix='USER', length=8):
        """Generate a user ID"""
        number = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        return f"{prefix}{number}"

    def username(self):
        """Generate a username"""
        first = self.generator.first_name().lower()
        last = self.generator.last_name().lower()

        patterns = [
            f"{first}{last}",
            f"{first}.{last}",
            f"{first}_{last}",
            f"{first}{last}{random.randint(1, 999)}",
            f"{first[0]}{last}"
        ]

        return random.choice(patterns)