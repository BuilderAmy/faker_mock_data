from faker.providers import BaseProvider
import random


class AddressUSProviderFull(BaseProvider):
    """Generate full US addresses with all components"""

    def full_address(self):
        """Generate a complete US address"""
        street = self.generator.street_address()
        city = self.generator.city()
        state = self.generator.state_abbr()
        zipcode = self.generator.zipcode()

        return {
            'street': street,
            'city': city,
            'state': state,
            'zip': zipcode,
            'full': f"{street}, {city}, {state} {zipcode}"
        }

    def apartment_number(self):
        """Generate apartment/unit number"""
        formats = [
            f"Apt {random.randint(1, 999)}",
            f"Unit {random.randint(1, 999)}",
            f"Suite {random.randint(100, 999)}",
            f"#{random.randint(1, 999)}"
        ]
        return random.choice(formats)


class PhoneNumberProviderNew(BaseProvider):
    """Generate phone numbers with various formats"""

    def phone_number(self, country='US', with_extension=False):
        """Generate a phone number"""
        if country == 'US':
            # US phone format: (XXX) XXX-XXXX
            area_code = random.randint(200, 999)
            exchange = random.randint(200, 999)
            subscriber = random.randint(1000, 9999)

            formats = [
                f"({area_code}) {exchange}-{subscriber}",
                f"{area_code}-{exchange}-{subscriber}",
                f"{area_code}.{exchange}.{subscriber}",
                f"+1-{area_code}-{exchange}-{subscriber}",
                f"{area_code}{exchange}{subscriber}"
            ]

            number = random.choice(formats)

            if with_extension and random.random() < 0.3:
                ext = random.randint(100, 9999)
                number += f" ext. {ext}"

            return number
        else:
            # International format
            country_code = random.randint(1, 999)
            number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            return f"+{country_code} {number}"

    def mobile_number(self):
        """Generate a mobile phone number"""
        # Mobile numbers typically start with certain area codes
        mobile_areas = [201, 202, 203, 310, 415, 510, 626, 650, 714, 818, 917, 929]
        area_code = random.choice(mobile_areas)
        exchange = random.randint(200, 999)
        subscriber = random.randint(1000, 9999)
        return f"({area_code}) {exchange}-{subscriber}"

    def toll_free_number(self):
        """Generate a toll-free number (800, 888, 877, 866, 855, 844, 833)"""
        toll_free_codes = [800, 888, 877, 866, 855, 844, 833]
        area_code = random.choice(toll_free_codes)
        exchange = random.randint(200, 999)
        subscriber = random.randint(1000, 9999)
        return f"1-{area_code}-{exchange}-{subscriber}"


class IpAddressProvider(BaseProvider):
    """Generate IP addresses"""

    def ipv4(self):
        """Generate an IPv4 address"""
        return '.'.join([str(random.randint(0, 255)) for _ in range(4)])

    def ipv6(self):
        """Generate an IPv6 address"""
        segments = []
        for _ in range(8):
            segment = ''.join(random.choices('0123456789abcdef', k=4))
            segments.append(segment)
        return ':'.join(segments)

    def private_ipv4(self):
        """Generate a private IPv4 address"""
        # Common private ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
        ranges = [
            lambda: f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            lambda: f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            lambda: f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ]
        return random.choice(ranges)()

    def mac_address(self):
        """Generate a MAC address"""
        segments = []
        for _ in range(6):
            segment = ''.join(random.choices('0123456789ABCDEF', k=2))
            segments.append(segment)
        return ':'.join(segments)