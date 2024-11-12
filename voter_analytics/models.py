from django.db import models
from django.utils.dateparse import parse_date

# Create your models here.

class Voter(models.Model):
    voter_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address_street_number = models.CharField(max_length=10)
    address_street_name = models.CharField(max_length=100)
    address_apartment = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=3)
    precinct_number = models.CharField(max_length=10)
    voter_score = models.IntegerField()

    # Boolean fields for election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.voter_id})"

    @staticmethod
    def load_data(file_path):
        import csv

        def parse_boolean(value):
            """Convert CSV strings 'TRUE' and 'FALSE' to boolean values."""
            if value is not None:
                value = value.strip().upper()
                if value == "TRUE":
                    return True
                elif value == "FALSE":
                    return False
            return False  # Default to False if value is None or doesn't match

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates to ensure correct format
                dob = parse_date(row['Date of Birth'])
                registration_date = parse_date(row['Date of Registration'])

                # Print parsed values for debugging
                print("Parsing row for Voter:", row['Voter ID Number'])
                print({
                    'v20state': parse_boolean(row.get('v20state')),
                    'v21town': parse_boolean(row.get('v21town')),
                    'v21primary': parse_boolean(row.get('v21primary')),
                    'v22general': parse_boolean(row.get('v22general')),
                    'v23town': parse_boolean(row.get('v23town'))
                })

                # Create a Voter record with correctly parsed booleans
                Voter.objects.create(
                    voter_id=row['Voter ID Number'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    address_street_number=row['Residential Address - Street Number'],
                    address_street_name=row['Residential Address - Street Name'],
                    address_apartment=row.get('Residential Address - Apartment Number', ''),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=dob,
                    date_of_registration=registration_date,
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    voter_score=int(row['voter_score']),
                    v20state=parse_boolean(row.get('v20state')),
                    v21town=parse_boolean(row.get('v21town')),
                    v21primary=parse_boolean(row.get('v21primary')),
                    v22general=parse_boolean(row.get('v22general')),
                    v23town=parse_boolean(row.get('v23town'))
                )