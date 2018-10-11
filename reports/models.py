from django.db import models


class Report(models.Model):
    created_time = models.DateTimeField(auto_now_add=True) # Datetime the report was created
    queued_time = models.DateTimeField(null=True, blank=True) # Datetime the report should be started
    start_time = models.DateTimeField(null=True, blank=True) # Datetime the report was started
    end_time = models.DateTimeField(null=True, blank=True) # Datetime the report finished
    REPORT_TYPE_CHOICES = (
        ("fixity", "Fixity"),
        ("format", "Format"),
    )
    report_type = models.CharField(choices=REPORT_TYPE_CHOICES, max_length=100)
    PROCESS_STATUS_CHOICES = (
        ("queued", "Report queued"),
        ("started", "Report started"),
        ("completed", "Report completed"),
    )
    process_status = models.CharField(choices=PROCESS_STATUS_CHOICES, max_length=100)
    items_checked = models.PositiveIntegerField(default=0)


class ReportItem(models.Model):
    file = models.CharField(max_length=512)
    uri = models.CharField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)


class FixityReportItem(ReportItem):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="fixity_report")
    verdict = models.CharField(max_length=10)


class FormatReportItem(ReportItem):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="format_report")
    file_format = models.CharField(max_length=256)
