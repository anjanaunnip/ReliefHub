from django.db import migrations


def seed_data(apps, schema_editor):
    DonationCategory = apps.get_model('home', 'DonationCategory')
    DonationItem = apps.get_model('home', 'DonationItem')

    data = {
    "Baby Food": [
        ("Baby formula (0-6 months)", 450),
        ("Baby formula (6+ months)", 480),
        ("Baby food purees (4-6 months)", 60),
        ("Baby food purees (6+ months)", 65),
        ("Baby cereals", 180),
        ("Baby snacks & finger foods", 90),
    ],

    "Clothing & Apparel": [
        ("Men's Clothing", 1200),
        ("Women's Clothing", 1400),
        ("Children's Clothing", 900),
        ("Winter Jackets", 2500),
        ("Blankets & Shawls", 1800),
        ("Footwear", 1500),
    ],

    "Medical Supplies": [
        ("First Aid Kit", 1800),
        ("Pain Relievers", 500),
        ("Paracetamol/Dolo", 350),
        ("ORS (Oral Rehydration Salts)", 450),
        ("Antibiotic Ointment", 600),
        ("Thermometer", 1200),
    ],

    "Hygiene & Sanitary Items": [
        ("Soap", 250),
        ("Sanitizer", 450),
        ("Tissue Paper", 350),
        ("Toothpaste & Brushes", 500),
        ("Hand Towels", 700),
        ("Toilet Paper", 600),
    ],

    "Water & Beverages": [
        ("Bottled Water", 500),
        ("Juice Boxes", 700),
        ("Milk Cartons", 650),
        ("Electrolyte Drinks", 900),
        ("Tea/Coffee Packets", 800),
        ("Energy Drinks", 1200),
    ],

    "Canned & Dry Foods": [
        ("Canned Beans", 600),
        ("Canned Vegetables", 550),
        ("Dry Rice", 1800),
        ("Dry Lentils", 1600),
        ("Pasta", 900),
        ("Biscuits", 700),
    ],

    "Shelter & Bedding": [
        ("Blankets", 1800),
        ("Pillows", 1200),
        ("Sleeping Bags", 3500),
        ("Tents", 7500),
        ("Bedsheets", 1800),
        ("Foam Mats", 1500),
    ],

    "Educational Supplies": [
        ("Notebooks", 500),
        ("Pens & Pencils", 350),
        ("School Bags", 1800),
        ("Geometry Kits", 450),
        ("Drawing Books", 500),
        ("Crayons", 400),
    ],

    "Cleaning Supplies": [
        ("Detergent Powder", 900),
        ("Mops", 1200),
        ("Toilet Cleaners", 650),
        ("Brushes", 500),
        ("Sanitizing Wipes", 750),
        ("Dishwashing Liquid", 600),
    ],
    }

    for category_name, items in data.items():
        category, _ = DonationCategory.objects.get_or_create(name=category_name)
        for item_name in items:
            DonationItem.objects.get_or_create(category=category, name=item_name)


def remove_data(apps, schema_editor):
    DonationCategory = apps.get_model('home', 'DonationCategory')
    DonationCategory.objects.filter(name__in=[
        "Baby Food", "Clothing & Apparel", "Medical Supplies",
        "Hygiene & Sanitary Items", "Water & Beverages", "Canned & Dry Foods",
        "Shelter & Bedding", "Educational Supplies", "Cleaning Supplies",
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_payment'),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_data),
    ]
