from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category,
    Donor,
    ReliefCamp,
    DonationCategory,
    DonationItem,
    DonationRequest,
    ReliefCampRequest,
)


# ----------------------------
# Basic registrations
# ----------------------------
admin.site.register(Donor)
admin.site.register(ReliefCamp)
admin.site.register(DonationCategory)

admin.site.register(DonationRequest)


# ----------------------------
# Category Admin (with icon preview)
# ----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_preview")
    search_fields = ("name",)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<i class="{}" style="font-size:20px;color:#d9534f;"></i>&nbsp;<small>{}</small>',
                obj.icon,
                obj.icon,
            )
        return "-"
    icon_preview.short_description = "Icon"


# ----------------------------
# ReliefCampRequest Admin (with auto-allocation)
# ----------------------------
@admin.register(ReliefCampRequest)
class ReliefCampRequestAdmin(admin.ModelAdmin):
    list_display = (
        "camp",
        "category",
        "item",
        "quantity",
        "unit",
        "urgency",
        "people",
        "date_needed",
        "status",
        "created_at",
    )
    list_filter = ("status", "urgency", "date_needed", "created_at", "category", "item")
    search_fields = (
        "category",
        "item__name",
        "camp__name",
        "location",
        "contact_person",
    )
    readonly_fields = ("created_at",)
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs["choices"] = [
                ("pending", "Pending"),
                ("allocated", "Allocated"),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


# ----------------------------
# DonationItem Admin (with price)
# ----------------------------
@admin.register(DonationItem)
class DonationItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")   # show price
    list_filter = ("category",)
    search_fields = ("name",)
