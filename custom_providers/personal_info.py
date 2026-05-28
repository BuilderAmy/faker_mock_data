"""
Personal Information Custom Providers
"""

from faker.providers import BaseProvider
import random
from datetime import datetime, timedelta


class PersonNameProvider(BaseProvider):
    """Generate person names with various formats"""

    def person_name(self, with_middle=False, with_suffix=False):
        """Generate a full person name"""
        first = self.generator.first_name()
        last = self.generator.last_name()

        name = f"{first} {last}"

        if with_middle:
            middle = fake.first_name()
            name = f"{first} {middle} {last}"

        if with_suffix:
            suffixes = ['Jr.', 'Sr.', 'II', 'III', 'IV']
            name += f" {random.choice(suffixes)}"

        return name


class NationalityProvider(BaseProvider):
    """Provide nationalities"""

    nationalities = [
        'American', 'Canadian', 'British', 'Australian', 'German',
        'French', 'Italian', 'Spanish', 'Mexican', 'Brazilian',
        'Indian', 'Chinese', 'Japanese', 'Korean', 'Russian',
        'Irish', 'Polish', 'Dutch', 'Swedish', 'Norwegian'
    ]

    def nationality(self):
        return random.choice(self.nationalities)


class EmailProvider(BaseProvider):
    """Generate email addresses"""

    domains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'icloud.com', 'protonmail.com', 'mail.com', 'aol.com'
    ]

    def email_address(self, name=None):
        """Generate an email address"""
        if not name:
            name = self.generator.first_name().lower() + self.generator.last_name().lower()
        else:
            name = name.lower().replace(' ', '.')

        domain = random.choice(self.domains)

        # Add random numbers sometimes
        if random.random() < 0.3:
            name += str(random.randint(1, 999))

        return f"{name}@{domain}"


class TimeProvider(BaseProvider):
    """Generate time-related data"""

    def time_of_day(self, format_24hr=False):
        """Generate a random time"""
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        if format_24hr:
            return f"{hour:02d}:{minute:02d}:{second:02d}"
        else:
            period = 'AM' if hour < 12 else 'PM'
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0:
                display_hour = 12
            return f"{display_hour:02d}:{minute:02d}:{second:02d} {period}"


class AgeProvider(BaseProvider):
    """Generate ages"""

    def age(self, min_age=18, max_age=90):
        """Generate a random age"""
        return random.randint(min_age, max_age)

    def age_group(self):
        """Return an age group category"""
        groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        return random.choice(groups)


class DOBProvider(BaseProvider):
    """Generate date of birth"""

    def date_of_birth(self, min_age=18, max_age=90):
        """Generate a date of birth"""
        today = datetime.now()
        age = random.randint(min_age, max_age)

        # Calculate birth year
        birth_year = today.year - age

        # Random month and day
        birth_month = random.randint(1, 12)

        # Handle days in month
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if birth_month == 2 and birth_year % 4 == 0:
            max_day = 29
        else:
            max_day = days_in_month[birth_month - 1]

        birth_day = random.randint(1, max_day)

        return datetime(birth_year, birth_month, birth_day).strftime("%Y-%m-%d")


class Gender(BaseProvider):
    """Provide gender information"""

    genders = ['Male', 'Female', 'Non-binary', 'Prefer not to say']

    def gender(self):
        return random.choice(self.genders)


class Orientation(BaseProvider):
    """Provide sexual orientation information"""

    orientations = [
        'Heterosexual', 'Homosexual', 'Bisexual', 'Pansexual',
        'Asexual', 'Prefer not to say'
    ]

    def orientation(self):
        return random.choice(self.orientations)


class Title(BaseProvider):
    """Provide personal titles"""

    titles = ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Rev.']

    def title(self):
        return random.choice(self.titles)


class MaritalStatus(BaseProvider):
    """Provide marital status"""

    statuses = [
        'Single', 'Married', 'Divorced', 'Widowed',
        'Separated', 'Domestic Partnership'
    ]

    def marital_status(self):
        return random.choice(self.statuses)


class Relation(BaseProvider):
    """Provide relationship types"""

    relations = [
        'Spouse', 'Parent', 'Child', 'Sibling', 'Grandparent',
        'Grandchild', 'Aunt', 'Uncle', 'Cousin', 'Nephew',
        'Niece', 'Friend', 'Colleague', 'Partner', 'Guardian'
    ]

    def relation(self):
        return random.choice(self.relations)