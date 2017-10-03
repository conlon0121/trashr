from dal import autocomplete
from django.contrib import admin
from django_admin_bootstrapped.admin.models import SortableInline
from base.models import IntervalReading, IntervalSet, Dumpster, Organization


class IntervalReadingAdmin(admin.ModelAdmin):
    pass


class IntervalReadingInline(admin.TabularInline):
    model = IntervalReading
    extra = 0


class IntervalSetAdmin(admin.ModelAdmin):
    list_display = ('timestamp',)
    inlines = [IntervalReadingInline]


class DumpsterAdmin(admin.ModelAdmin):
    pass


class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(IntervalReading, IntervalReadingAdmin)
admin.site.register(Dumpster, DumpsterAdmin)
admin.site.register(IntervalSet, IntervalSetAdmin)
