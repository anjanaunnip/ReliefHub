from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    ROLE_CHOICES = [
        ('donour', 'Donor'),
        ('reliefcamp', 'ReliefCamp'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default="user")  # ✅ Default value
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class ReliefCamp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reliefcamp_profile")
    name = models.CharField(max_length=150, default="Unnamed Relief Camp")  # ✅ Default value
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.location})"


class DonationCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True)  # for UI icon

    def __str__(self):
        return self.name


class DonationItem(models.Model):
    category = models.ForeignKey(DonationCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 💰 New field

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class DonationRequest(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    item = models.ForeignKey(DonationItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    expiry_date = models.DateField(blank=True, null=True)
    pickup_location = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    preferred_pickup_time = models.CharField(max_length=100, blank=True)
    urgency_level = models.CharField(max_length=30)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.name} - {self.item.name} ({self.quantity} {self.unit})"


ICON_CHOICES = [
    ('fa-solid fa-bottle-baby', 'Baby Food'),
    ('fa-solid fa-shirt', 'Clothing & Apparel'),
    ('fa-solid fa-kit-medical', 'Medical Supplies'),
    ('fa-solid fa-soap', 'Hygiene & Sanitary Items'),
    ('fa-solid fa-tint', 'Water & Beverages'),
    ('fa-solid fa-can-food', 'Canned & Dry Foods'),
    ('fa-solid fa-bed', 'Shelter & Bedding'),
    ('fa-solid fa-book', 'Educational Supplies'),
    ('fa-solid fa-broom', 'Cleaning Supplies'),
]


class Category(models.Model):
    name = models.CharField(max_length=150)
    icon = models.CharField(
        max_length=120,
        choices=ICON_CHOICES,
        blank=True,
        null=True,
        help_text="Font Awesome classes, e.g. 'fa-solid fa-bottle-baby'"
    )

    def __str__(self):
        return self.name


class ReliefCampRequest(models.Model):
    camp = models.ForeignKey("ReliefCamp", on_delete=models.CASCADE, related_name="requests")

    # Aid details
    category = models.CharField(max_length=100, default="General")
    item = models.ForeignKey(      # ✅ add link to DonationItem
        "DonationItem",
        on_delete=models.CASCADE,
        related_name="camp_requests",
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, default="units")
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)


    # Priority
    urgency = models.CharField(
        max_length=20,
        choices=[("Normal", "Normal"), ("High", "High"), ("Urgent", "Urgent")],
        default="Normal"
    )
    people = models.PositiveIntegerField(default=0)

    # Location & timeline
    date_needed = models.DateField(default="2000-01-01")  # ✅ Safe default, replace later
    location = models.CharField(max_length=255, default="Unknown")

    # Contact
    contact_person = models.CharField(max_length=100, default="General")
    phone = models.CharField(max_length=20, default="0000000000")

    # Notes
    justification = models.TextField(default="Not provided")
    notes = models.TextField(blank=True)

    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("allocated", "Allocated"),   # ✅ added new status
        
        ],
        default="pending"
    )

    #allocation details listing
    allocated_donation = models.ForeignKey(
        "DonationRequest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="allocated_requests"
    )

    def __str__(self):
        return f"{self.category} - {self.item} ({self.camp.name})"
    

class Payment(models.Model):
    request = models.OneToOneField("ReliefCampRequest", on_delete=models.CASCADE, related_name="payment")
    payer = models.ForeignKey("Donor", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_payment_id = models.CharField(max_length=200)
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_signature = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.request.id} - {self.amount}"
