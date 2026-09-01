from django.db import migrations


def seed_data(apps, schema_editor):
    DonationCategory = apps.get_model('home', 'DonationCategory')
    DonationItem = apps.get_model('home', 'DonationItem')

    data = {
        "Baby Food": [
            "Baby formula (0-6 months)", "Baby formula (6+ months)",
            "Baby food purees (4-6 months)", "Baby food purees (6+ months)",
            "Baby cereals", "Baby snacks & finger foods",
        ],
        "Clothing & Apparel": [
            "Men's Clothing", "Women's Clothing", "Children's Clothing",
            "Winter Jackets", "Blankets & Shawls", "Footwear",
        ],
        "Medical Supplies": [
            "First Aid Kit", "Pain Relievers", "Paracetamol/Dolo",
            "ORS (Oral Rehydration Salts)", "Antibiotic Ointment", "Thermometer",
        ],
        "Hygiene & Sanitary Items": [
            "Soap", "Sanitizer", "Tissue Paper",
            "Toothpaste & Brushes", "Hand Towels", "Toilet Paper",
        ],
        "Water & Beverages": [
            "Bottled Water", "Juice Boxes", "Milk Cartons",
            "Electrolyte Drinks", "Tea/Coffee Packets", "Energy Drinks",
        ],
        "Canned & Dry Foods": [
            "Canned Beans", "Canned Vegetables", "Dry Rice",
            "Dry Lentils", "Pasta", "Biscuits",
        ],
        "Shelter & Bedding": [
            "Blankets", "Pillows", "Sleeping Bags",
            "Tents", "Bedsheets", "Foam Mats",
        ],
        "Educational Supplies": [
            "Notebooks", "Pens & Pencils", "School Bags",
            "Geometry Kits", "Drawing Books", "Crayons",
        ],
        "Cleaning Supplies": [
            "Detergent Powder", "Mops", "Toilet Cleaners",
            "Brushes", "Sanitizing Wipes", "Dishwashing Liquid",
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
