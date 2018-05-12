from django.contrib import admin
from trashr.models import (IntervalReading, Dumpster, Organization, UserProfile, Email, PaymentMethod,
                           Alert, Pickup, Product, Plan, Subscription, Transaction)


@admin.register(IntervalReading)
class IntervalReadingAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'raw_readings')


@admin.register(Dumpster)
class DumpsterAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass


@admin.register(Pickup)
class PickupAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
