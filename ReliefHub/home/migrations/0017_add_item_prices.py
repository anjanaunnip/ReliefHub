from django.db import migrations


def add_prices(apps, schema_editor):
    DonationItem = apps.get_model('home', 'DonationItem')

    prices = {
        "Baby formula (0-6 months)": 450, "Baby formula (6+ months)": 480,
        "Baby food purees (4-6 months)": 60, "Baby food purees (6+ months)": 65,
        "Baby cereals": 180, "Baby snacks & finger foods": 90,

        "Men's Clothing": 400, "Women's Clothing": 400, "Children's Clothing": 300,
        "Winter Jackets": 900, "Blankets & Shawls": 500, "Footwear": 600,

        "First Aid Kit": 350, "Pain Relievers": 40, "Paracetamol/Dolo": 30,
        "ORS (Oral Rehydration Salts)": 20, "Antibiotic Ointment": 60, "Thermometer": 150,

        "Soap": 30, "Sanitizer": 80, "Tissue Paper": 40,
        "Toothpaste & Brushes": 70, "Hand Towels": 100, "Toilet Paper": 60,

        "Bottled Water": 20, "Juice Boxes": 25, "Milk Cartons": 55,
        "Electrolyte Drinks": 30, "Tea/Coffee Packets": 150, "Energy Drinks": 40,

        "Canned Beans": 60, "Canned Vegetables": 55, "Dry Rice": 70,
        "Dry Lentils": 90, "Pasta": 50, "Biscuits": 30,

        "Blankets": 400, "Pillows": 250, "Sleeping Bags": 1200,
        "Tents": 3500, "Bedsheets": 350, "Foam Mats": 600,

        "Notebooks": 40, "Pens & Pencils": 20, "School Bags": 500,
        "Geometry Kits": 100, "Drawing Books": 60, "Crayons": 80,

        "Detergent Powder": 90, "Mops": 200, "Toilet Cleaners": 80,
        "Brushes": 50, "Sanitizing Wipes": 100, "Dishwashing Liquid": 70,
    }

    for item_name, item_price in prices.items():
        DonationItem.objects.filter(name=item_name).update(price=item_price)


def reverse_prices(apps, schema_editor):
    DonationItem = apps.get_model('home', 'DonationItem')
    DonationItem.objects.all().update(price=0.00)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_seed_donation_data'),
    ]

    operations = [
        migrations.RunPython(add_prices, reverse_prices),
    ]
