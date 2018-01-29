from django.contrib import admin
from trashr.models import IntervalReading, Dumpster, Organization


class IntervalReadingAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'raw_readings')


class DumpsterAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    pass


class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(IntervalReading, IntervalReadingAdmin)
admin.site.register(Dumpster, DumpsterAdmin)

