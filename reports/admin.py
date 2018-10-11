from django.contrib import admin

from reports.models import *


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(FixityReportItem)
class FixityReportItemAdmin(admin.ModelAdmin):
    pass


@admin.register(FormatReportItem)
class FixityReportItemAdmin(admin.ModelAdmin):
    pass
