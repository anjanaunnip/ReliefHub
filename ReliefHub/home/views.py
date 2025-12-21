# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



# Models used across the views
from .models import (
    Donor,
    ReliefCamp,
    ReliefCampRequest,
    DonationCategory,
    DonationItem,
    DonationRequest,
    Payment,
)


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# -------------------------
# Public / auth views
# -------------------------
def index(request):
    return render(request, 'home.html')





def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        password = request.POST.get("password")
        confirm_pw = request.POST.get("confirmpw")
        role = request.POST.get("role")   # 'donour' or 'reliefcamp'

        context = {"form_data": request.POST}  # ✅ preserve entered data

        # 1. Required fields
        if not fullname or not email or not phone or not location or not password or not confirm_pw or not role:
            messages.error(request, "All fields are required!")
            return render(request, "register.html", context)

        # 2. Fullname validation → no spaces, allow letters , underscores
        if not re.match(r'^[A-Za-z_]+$', fullname):
            messages.error(request, "Name must not contain spaces. Use underscore (_) instead.")
            return render(request, "register.html", context)

        # 3. Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return render(request, "register.html", context)

        # 4. Phone validation → must be exactly 10 digits
        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, "register.html", context)

        # 5. Password validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "register.html", context)

        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            messages.error(request, "Password must contain both letters and numbers.")
            return render(request, "register.html", context)

        # 6. Confirm password match
        if password != confirm_pw:
            messages.error(request, "Passwords do not match!")
            return render(request, "register.html", context)

        # 7. Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, "register.html", context)

        # ✅ Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )

        # Save based on chosen role
        if role == "donour":
            Donor.objects.create(
                user=user,
                name=fullname,
                role="donour",
                phone=phone,
                location=location
            )
        elif role == "reliefcamp":
            ReliefCamp.objects.create(
                user=user,
                name=fullname,
                phone=phone,
                location=location
            )

        messages.success(request, "Registration successful! You can log in now.")
        return redirect("login")

    # First-time load → no prefilled data
    return render(request, "register.html", {"form_data": {}})



def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "All fields are required!")
            return render(request, "login.html")

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password!")
            return render(request, "login.html")

        # Check ReliefCamp and Donor profiles
        camp_profile = ReliefCamp.objects.filter(user=user).first()
        donor_profile = Donor.objects.filter(user=user).first()

        login(request, user)

        if camp_profile:
            return redirect("campdashboard")
        elif donor_profile:
            return redirect("donourdashboard")
        else:
            messages.error(request, "No profile found for this account.")
            return render(request, "login.html")

    return render(request, "login.html")


# -------------------------
# Donor / donation views
# -------------------------
@login_required
def donourdashboard(request):
    categories = DonationCategory.objects.all()
    items_preview = DonationItem.objects.all()[:6]

    # ✅ Fetch relief camp requests that are still pending
    relief_requests = ReliefCampRequest.objects.filter(status="pending").order_by("-created_at")

    return render(request, "donation_categories.html", {
        "categories": categories,
        "items_preview": items_preview,
        "relief_requests": relief_requests,   # pass to template
    })



@login_required
def donation_categories(request):
    categories = DonationCategory.objects.all()
    return render(request, 'donation_categories.html', {'categories': categories})


@login_required
def select_donation_item(request, cat_id):
    category = get_object_or_404(DonationCategory, id=cat_id)
    items = DonationItem.objects.filter(category=category)
    return render(request, "select_donation_item.html", {
        "category": category,
        "items": items
    })


@login_required
def donation_details(request, item_id):
    item = get_object_or_404(DonationItem, id=item_id)
    donor_profile = Donor.objects.get(user=request.user)

    req_id = request.GET.get("req_id")  # ✅ relief request id if donating from notification
    camp_request = None
    if req_id:
        camp_request = ReliefCampRequest.objects.filter(id=req_id, status="pending").first()

    if request.method == "POST":
        donation = DonationRequest.objects.create(
            donor=donor_profile,
            item=item,
            quantity=request.POST.get("quantity"),
            unit=request.POST.get("unit"),
            expiry_date=request.POST.get("expiry_date") or None,
            pickup_location=request.POST.get("pickup_location"),
            contact_person=request.POST.get("contact_person"),
            phone_number=request.POST.get("phone_number"),
            preferred_pickup_time=request.POST.get("preferred_pickup_time"),
            urgency_level=request.POST.get("urgency_level"),
            special_instructions=request.POST.get("special_instructions"),
        )

        # ✅ If this donation is from a relief camp request, allocate it
        if camp_request:
            camp_request.allocated_donation = donation
            camp_request.status = "allocated"
            camp_request.save()

        return redirect("donation_thankyou")

    return render(request, "donation_details.html", {
        "item": item,
        "camp_request": camp_request,   # you can use this to pre-fill fields if needed
    })



@login_required
def donation_thankyou(request):
    return render(request, "donation_thankyou.html")


# -------------------------
# Camp dashboard & requests
# -------------------------
@login_required
def campdashboard(request):
    camp_profile = ReliefCamp.objects.get(user=request.user)

    # All requests for this camp
    requests_qs = ReliefCampRequest.objects.filter(camp=camp_profile)

    # Counts
    total_requests = requests_qs.count()
    pending_count = requests_qs.filter(status="pending").count()
    allocated_count = requests_qs.filter(status="allocated").count()

    # Recent activity (latest 5 requests)
    recent_activity = requests_qs.order_by("-created_at")[:5]

    return render(request, "reliefcamp.html", {
        "camp_profile": camp_profile,
        "total_requests": total_requests,
        "pending_count": pending_count,
        "allocated_count": allocated_count,
        "recent_activity": recent_activity,
    })




def custom_logout(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def my_requests(request):
    camp_profile = get_object_or_404(ReliefCamp, user=request.user)
    requests_qs = ReliefCampRequest.objects.filter(camp=camp_profile).order_by("-created_at")

    return render(
        request,
        "my_requests.html",
        {
            "camp_profile": camp_profile,
            "requests": requests_qs
        }
    )



@login_required
def new_requests(request):
    camp_profile = ReliefCamp.objects.get(user=request.user)
    categories = DonationCategory.objects.all()
    selected_category = None
    items = None

    if request.method == "POST":
        category_id = request.POST.get("category")
        item_id = request.POST.get("item")

        # Case 1: category selected but no item yet
        if category_id and not item_id:
            selected_category = get_object_or_404(DonationCategory, id=category_id)
            items = DonationItem.objects.filter(category=selected_category)
            return render(request, "new_requests.html", {
                "camp_profile": camp_profile,
                "categories": categories,
                "selected_category": selected_category,
                "items": items,
                "form_data": request.POST,
            })

        # Case 2: full form submitted
        if category_id and item_id:
            category = get_object_or_404(DonationCategory, id=category_id)
            item = get_object_or_404(DonationItem, id=item_id)
            quantity_requested = int(request.POST.get("quantity"))

            camp_request = ReliefCampRequest.objects.create(
                camp=camp_profile,
                category=category.name,
                item=item,
                quantity=quantity_requested,
                unit=request.POST.get("unit"),
                urgency=request.POST.get("urgency"),
                people=request.POST.get("people"),
                date_needed=request.POST.get("date_needed"),
                location=request.POST.get("location"),
                contact_person=request.POST.get("contact_person"),
                phone=request.POST.get("phone"),
                justification=request.POST.get("justification"),
                notes=request.POST.get("notes") or "",
            )

            # ✅ Try to auto-allocate
            donation = DonationRequest.objects.filter(
                item=item,
                unit__iexact=camp_request.unit,
                quantity__gt=0
            ).order_by("created_at").first()

            if donation:
                if donation.quantity >= camp_request.quantity:
                    donation.quantity -= camp_request.quantity
                    camp_request.status = "allocated"
                else:
                    camp_request.quantity = donation.quantity
                    donation.quantity = 0
                    camp_request.status = "allocated"

                # ✅ Link allocated donation
                camp_request.allocated_donation = donation
                donation.save()
                camp_request.save()

            messages.success(request, "Your request has been submitted.")
            return redirect("reliefcamp_thankyou")

    return render(request, "new_requests.html", {
        "camp_profile": camp_profile,
        "categories": categories,
        "selected_category": selected_category,
        "items": items,
    })

@login_required
def reliefcamp_thankyou(request):
    return render(request, "reliefcamp_thankyou.html")

@login_required
def donate_from_request(request, req_id):
    camp_request = get_object_or_404(ReliefCampRequest, id=req_id, status="pending")

    # ✅ Redirect to donation_details but pass req_id as query param
    return redirect(f"/donate/item/{camp_request.item.id}/?req_id={camp_request.id}")



@login_required
def pay_now(request, req_id):
    camp_request = get_object_or_404(ReliefCampRequest, id=req_id, status="pending")

    # ✅ Fetch price from DonationItem model
    amount_per_unit = camp_request.item.price
    total_amount = float(amount_per_unit) * camp_request.quantity * 100  # convert to paise

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_order = client.order.create({
        "amount": int(total_amount),  # Razorpay requires integer paise
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save order_id to DB
    camp_request.razorpay_order_id = payment_order["id"]
    camp_request.save()

    context = {
        "camp_request": camp_request,
        "order_id": payment_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": int(total_amount),  # pass paise to Razorpay
        "currency": "INR",
        "unit_price": amount_per_unit,  # ✅ send to template
        "total_display": float(amount_per_unit) * camp_request.quantity,  # ₹ display only
    }
    return render(request, "pay_now.html", context)



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        order_id = data.get("razorpay_order_id")

        # Find camp request
        camp_request = ReliefCampRequest.objects.filter(razorpay_order_id=order_id).first()

        if camp_request:
            # Calculate amount (in rupees)
            amount_paid = (camp_request.item.price * camp_request.quantity)

            # Create Payment record
            Payment.objects.create(
                request=camp_request,
                payer=request.user.donor,   # logged-in donor
                amount=amount_paid,
                razorpay_payment_id=data.get("razorpay_payment_id"),
                razorpay_order_id=order_id,
                razorpay_signature=data.get("razorpay_signature")
            )

            # Mark as allocated
            camp_request.status = "allocated"
            camp_request.save()

            return JsonResponse({"status": "success", "message": "Payment successful!"})

    return JsonResponse({"status": "error", "message": "Invalid request"})
