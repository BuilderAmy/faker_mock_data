"""
Social, Professional, and Miscellaneous Custom Providers
"""

from faker import Faker
from faker.providers import BaseProvider
import random
import string
from datetime import datetime


class USPoliticalParties(BaseProvider):
    """US Political party affiliation"""

    parties = [
        'Democratic Party', 'Republican Party', 'Independent',
        'Libertarian Party', 'Green Party', 'No Affiliation',
        'Other', 'Prefer not to say'
    ]

    def political_party(self):
        return random.choice(self.parties)


class IdeologyProvider(BaseProvider):
    """Political ideology"""

    ideologies = [
        'Liberal', 'Conservative', 'Moderate', 'Progressive',
        'Libertarian', 'Socialist', 'Centrist', 'Independent',
        'Prefer not to say'
    ]

    def ideology(self):
        return random.choice(self.ideologies)


class VulnerableCommunity(BaseProvider):
    """Vulnerable community classifications"""

    communities = [
        'Low Income', 'Elderly', 'Disabled', 'Minority',
        'Veterans', 'Homeless', 'Refugees', 'Children',
        'Single Parents', 'LGBTQ+', 'None'
    ]

    def vulnerable_community(self):
        return random.choice(self.communities)


class ReligionProvider(BaseProvider):
    """Religious affiliation"""

    religions = [
        'Christianity', 'Islam', 'Judaism', 'Hinduism', 'Buddhism',
        'Sikhism', 'Atheism', 'Agnosticism', 'Other', 'Prefer not to say'
    ]

    def religion(self):
        return random.choice(self.religions)


class JobProvider(BaseProvider):
    """Job titles and employment information"""

    job_titles = [
        'Software Engineer', 'Data Analyst', 'Project Manager', 'Sales Manager',
        'Marketing Specialist', 'Accountant', 'Teacher', 'Nurse', 'Doctor',
        'Lawyer', 'Consultant', 'Designer', 'Chef', 'Electrician',
        'Plumber', 'Police Officer', 'Firefighter', 'Retail Manager',
        'Customer Service Rep', 'HR Manager', 'Business Analyst', 'Architect'
    ]

    employment_statuses = [
        'Full-time', 'Part-time', 'Contract', 'Freelance',
        'Self-employed', 'Unemployed', 'Retired', 'Student'
    ]

    def job_title(self):
        return random.choice(self.job_titles)

    def employment_status(self):
        return random.choice(self.employment_statuses)


class SkillSet(BaseProvider):
    """Skills and competencies"""

    skills = [
        'Python', 'Java', 'JavaScript', 'SQL', 'Data Analysis',
        'Project Management', 'Communication', 'Leadership', 'Problem Solving',
        'Critical Thinking', 'Teamwork', 'Time Management', 'Customer Service',
        'Sales', 'Marketing', 'Accounting', 'Design', 'Writing', 'Public Speaking'
    ]

    def skill(self):
        return random.choice(self.skills)

    def skills_list(self, count=3):
        return random.sample(self.skills, min(count, len(self.skills)))


class RandomStarter(BaseProvider):
    """Random starter words/phrases"""

    starters = [
        'Welcome', 'Hello', 'Greetings', 'Dear', 'Attention',
        'Notice', 'Alert', 'Important', 'Urgent', 'Reminder'
    ]

    def starter(self):
        return random.choice(self.starters)


class AlphanumericProvider(BaseProvider):
    """Generate alphanumeric strings"""

    def alphanumeric(self, length=10, uppercase=True, lowercase=True, digits=True):
        """Generate random alphanumeric string"""
        chars = ''
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if digits:
            chars += string.digits

        return ''.join(random.choices(chars, k=length))


class Separator(BaseProvider):
    """Separator characters"""

    separators = [' ', '-', '_', '/', '|', '.', ',', ';']

    def separator(self):
        return random.choice(self.separators)


class SessionIDProvider(BaseProvider):
    """Generate session IDs"""

    def session_id(self):
        """Generate a session ID"""
        timestamp = int(datetime.now().timestamp())
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return f"SESSION-{timestamp}-{random_part}"


class FilenameProvider(BaseProvider):
    """Generate filenames"""

    extensions = [
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv',
        '.jpg', '.png', '.gif', '.mp4', '.mp3', '.zip', '.rar'
    ]

    file_types = [
        'report', 'invoice', 'statement', 'receipt', 'contract',
        'document', 'image', 'photo', 'video', 'audio', 'backup'
    ]

    def filename(self, with_extension=True):
        """Generate a filename"""
        file_type = random.choice(self.file_types)
        date = datetime.now().strftime("%Y%m%d")
        number = random.randint(1000, 9999)

        name = f"{file_type}_{date}_{number}"

        if with_extension:
            ext = random.choice(self.extensions)
            name += ext

        return name


class ProfileIDProvider(BaseProvider):
    """Generate profile IDs"""

    def profile_id(self):
        """Generate a profile ID"""
        prefix = random.choice(['PROF', 'USR', 'ACC', 'MEM'])
        number = random.randint(100000, 999999)
        return f"{prefix}-{number}"


class TimestampProvider(BaseProvider):
    """Generate timestamps"""

    def timestamp(self, format='iso'):
        """Generate a timestamp"""
        now = datetime.now()

        if format == 'iso':
            return now.isoformat()
        elif format == 'unix':
            return int(now.timestamp())
        elif format == 'datetime':
            return now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return now.strftime(format)


class CustomURLProvider(BaseProvider):
    """Generate URLs"""

    protocols = ['http://', 'https://']
    domains = ['example.com', 'test.com', 'demo.org', 'sample.net', 'site.co']
    paths = ['profile', 'user', 'account', 'dashboard', 'settings', 'help', 'support']

    def url(self, with_path=True, with_params=False):
        """Generate a URL"""
        protocol = random.choice(self.protocols)
        domain = random.choice(self.domains)

        url = protocol + domain

        if with_path:
            path = random.choice(self.paths)
            user_id = random.randint(1000, 9999)
            url += f"/{path}/{user_id}"

        if with_params:
            param_key = random.choice(['id', 'ref', 'token', 'session'])
            param_value = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            url += f"?{param_key}={param_value}"

        return url


class TeamsProvider(BaseProvider):
    """Team/department names"""

    teams = [
        'Engineering', 'Sales', 'Marketing', 'Finance', 'HR',
        'Operations', 'Customer Support', 'Product', 'Legal',
        'IT', 'Research', 'Development', 'Quality Assurance'
    ]

    def team(self):
        return random.choice(self.teams)


class LawProvider(BaseProvider):
    """Legal terms and regulations"""

    laws = [
        'GDPR', 'CCPA', 'HIPAA', 'SOX', 'PCI-DSS',
        'FERPA', 'COPPA', 'ADA', 'FCRA', 'GLBA'
    ]

    legal_terms = [
        'Terms of Service', 'Privacy Policy', 'User Agreement',
        'Cookie Policy', 'Data Protection Policy', 'Consent Form',
        'Disclaimer', 'License Agreement'
    ]

    def law(self):
        return random.choice(self.laws)

    def legal_term(self):
        return random.choice(self.legal_terms)


class ProductsProvider(BaseProvider):
    """Product names and categories"""

    categories = [
        'Electronics', 'Clothing', 'Food & Beverage', 'Home & Garden',
        'Sports & Outdoors', 'Books', 'Toys & Games', 'Health & Beauty',
        'Automotive', 'Office Supplies', 'Pet Supplies', 'Software'
    ]

    products = [
        'Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera',
        'T-Shirt', 'Jeans', 'Shoes', 'Watch', 'Backpack',
        'Coffee Maker', 'Blender', 'Vacuum', 'Lamp', 'Chair'
    ]

    def product_category(self):
        return random.choice(self.categories)

    def product_name(self):
        return random.choice(self.products)

    def product_sku(self):
        """Generate a product SKU"""
        prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
        number = random.randint(10000, 99999)
        return f"{prefix}-{number}"