from django.contrib import admin
from trashr.models import IntervalReading, Dumpster, Organization, UserProfile, Email


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
