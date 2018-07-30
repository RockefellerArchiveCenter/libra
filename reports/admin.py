from django.contrib import admin

from reports.models import *


@admin.register(FixityReport)
class FixityReportAdmin(admin.ModelAdmin):
    pass


@admin.register(FormatReport)
class FormatReportAdmin(admin.ModelAdmin):
    pass


@admin.register(FixityReportItem)
class FixityReportItemAdmin(admin.ModelAdmin):
    pass


@admin.register(FormatReportItem)
class FixityReportItemAdmin(admin.ModelAdmin):
    pass
