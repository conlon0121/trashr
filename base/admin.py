from dal import autocomplete
from django.contrib import admin
from django_admin_bootstrapped.admin.models import SortableInline
from base.models import IntervalReading, Dumpster, Organization
from django.contrib.auth.decorators import login_required


class IntervalReadingAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'raw_reading')


class DumpsterAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    pass


class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(IntervalReading, IntervalReadingAdmin)
admin.site.register(Dumpster, DumpsterAdmin)

